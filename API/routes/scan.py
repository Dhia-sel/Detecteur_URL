from datetime import datetime
from pathlib import Path
from threading import Lock, Thread
import traceback

from fastapi import APIRouter, HTTPException

from API.schema.scan_schema import ScanRequest
from App.Core.classifier import URLClassifier
from App.Core.normalizer import URLNormalizer
from App.Core.pipeline import URLAnalyzerPipeline
from App.Explaining.formatter import calculate_rule_risk_score
from ML import phishing_model


router = APIRouter(prefix="/api", tags=["scan"])
ML_LOG_PATH = Path(__file__).resolve().parents[2] / "ML" / "ml_training.log"
_ml_lock = Lock()
_ml_state = {
	"status": "ready" if phishing_model.MODEL_PATH.exists() else "idle",
	"message": "Modèle prêt." if phishing_model.MODEL_PATH.exists() else "Le modèle sera entraîné au premier scan.",
	"error": None,
}


def _set_ml_state(status, message, error=None, details=None):
	global _ml_state
	entry = f"{datetime.now().astimezone().isoformat(timespec='seconds')} [{status}] {message}"
	if error:
		entry += f" Détail: {error}"
	if details:
		entry += f"\n{details.rstrip()}"
	with _ml_lock:
		_ml_state = {"status": status, "message": message, "error": error}
		with ML_LOG_PATH.open("a", encoding="utf-8") as log_file:
			log_file.write(entry + "\n")


def _train_ml_model():
	try:
		phishing_model.train(progress_callback=_set_ml_state)
	except Exception as error:
		_set_ml_state(
			"error",
			"L'entraînement ML a échoué.",
			str(error),
			"".join(traceback.format_exception(error)),
		)


def _start_ml_training():
	global _ml_state
	with _ml_lock:
		if _ml_state["status"] in {"training", "downloading_dataset", "loading_dataset", "dataset_ready"}:
			return
		if phishing_model.MODEL_PATH.exists():
			return
		_ml_state = {"status": "training", "message": "Préparation du modèle ML.", "error": None}
		with ML_LOG_PATH.open("a", encoding="utf-8") as log_file:
			log_file.write(
				f"{datetime.now().astimezone().isoformat(timespec='seconds')} "
				"[training] Préparation du modèle ML.\n"
			)
	Thread(target=_train_ml_model, name="urlshield-ml-training", daemon=True).start()


def _get_ml_result(url, start_training=False, url_type=None):
	if url_type is None:
		normalized_url = URLNormalizer(url).normalize_url()
		url_type = URLClassifier(normalized_url).classify()
	if url_type not in {"hierarchical", "hiérarchique"}:
		return {
			"status": "unsupported",
			"message": "Le modèle ML est entraîné pour les URL web HTTP(S) hiérarchiques; cette URL est évaluée par les règles.",
			"score": None,
			"verdict": None,
			"error": None,
		}
	if phishing_model.MODEL_PATH.exists():
		try:
			score = phishing_model.phishing_percent(url)
			return {"status": "ready", "message": "Prédiction ML terminée.", "score": score,
				"verdict": phishing_model.verdict(score), "error": None}
		except Exception as error:
			_set_ml_state("error", "La prédiction ML a échoué.", str(error))
	elif start_training:
		_start_ml_training()

	with _ml_lock:
		return {**_ml_state, "score": None, "verdict": None}


@router.post("/scan")
def scan_url(payload: ScanRequest):
	url = payload.url.strip()
	if not url:
		raise HTTPException(status_code=422, detail="URL is required")

	result = URLAnalyzerPipeline(url).run()
	if not result.get("success"):
		raise HTTPException(status_code=422, detail=result.get("error", "URL analysis failed"))

	ml_result = _get_ml_result(url, start_training=True, url_type=result["url_type"])
	if ml_result["status"] == "unsupported":
		ml_result.update(calculate_rule_risk_score(result["report"]["data"]))
	return {
		"url": url,
		"ml": ml_result,
		**result,
	}


@router.post("/ml/score")
def score_url(payload: ScanRequest):
	url = payload.url.strip()
	if not url:
		raise HTTPException(status_code=422, detail="URL is required")
	return _get_ml_result(url)

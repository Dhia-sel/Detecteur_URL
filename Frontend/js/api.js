const API_BASE_URL = 'http://127.0.0.1:8000/api';

function escapeReportValue(value) {
	if (typeof value === 'string') {
		return value.replace(/[&<>"']/g, character => ({
			'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
		})[character]);
	}
	if (Array.isArray(value)) return value.map(escapeReportValue);
	if (value && typeof value === 'object') {
		return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, escapeReportValue(item)]));
	}
	return value;
}

const REPORT_FIELD_LABELS = {
	schema: 'Scheme',
	'schéma': 'Scheme',
	auteur: 'Authentication',
	auth: 'Authentication',
	utilisateur: 'Username',
	username: 'Username',
	'mot de passe': 'Password',
	password: 'Password',
	'le hote': 'Host',
	hote: 'Host',
	host: 'Host',
	port: 'Port',
	chemin: 'Path',
	path: 'Path',
	requete: 'Query',
	query: 'Query',
	fragment: 'Fragment',
	type_media: 'Media type',
	longueur_donnees: 'Payload length',
	donnees: 'Data preview',
	donnees_totales: 'Data payload',
	donnees_decodes: 'Decoded data',
	base64: 'Base64 encoded',
	type: 'URL type',
	enveloppe: 'Wrapper',
	clef: 'Parameter',
	'vrai url': 'Destination URL',
	destination: 'Destination',
	options: 'Query parameters'
};

function humanizeReportField(key) {
	const normalized = key.toLowerCase().trim();
	const label = REPORT_FIELD_LABELS[normalized] || normalized.replace(/_/g, ' ');
	return label.replace(/\b\w/g, character => character.toUpperCase());
}

function flattenReportFields(value, parents = [], result = {}) {
	for (const [key, item] of Object.entries(value || {})) {
		const normalizedKey = key.toLowerCase();
		if (item && typeof item === 'object' && !Array.isArray(item)) {
			const nextParents = ['auth', 'auteur'].includes(normalizedKey)
				? parents
				: [...parents, normalizedKey];
			flattenReportFields(item, nextParents, result);
		} else {
				if (item === null || item === undefined || item === '') continue;
			const label = humanizeReportField(key);
			const parent = parents[parents.length - 1];
			const displayLabel = parent === 'enveloppe'
				? `Wrapper ${label}`
				: parent === 'options'
					? `Parameter ${humanizeReportField(key)}`
					: label;
			result[escapeReportValue(displayLabel)] = Array.isArray(item) ? item.join(', ') : item;
		}
	}
	return result;
}

async function scanUrl(url) {
 const response = await fetch(`${API_BASE_URL}/scan`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ url })
	});

	const payload = await response.json();
	if (!response.ok) {
		throw new Error(payload.detail || payload.error || 'URL analysis failed');
	}
	if (!payload.success || !payload.report) {
		throw new Error(payload.error || 'URL analysis failed');
	}

	 return adaptReport(payload.report, payload.ml);
}

	async function getMlScore(url) {
		const response = await fetch(`${API_BASE_URL}/ml/score`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ url })
		});
		const payload = await response.json();
		if (!response.ok) throw new Error(payload.detail || payload.error || 'ML prediction failed');
		return payload;
	}

	function adaptReport(report, ml = {}) {
	const data = report.data || {};
	const lexical = data.lexical || {};
	const behaviour = data.behaviour || {};
	const address = data.address || {};
	const rawParsedUrl = report.parsed_url || {};
	const parsedUrl = flattenReportFields(escapeReportValue(rawParsedUrl));
	const scheme = rawParsedUrl.schema || rawParsedUrl['schéma'] || '';

	const recommendation = report.recommendation || '';

	const normalizedLexical = {
		...lexical,
		semantic_score: lexical.semantic_score ?? lexical.keywords ?? 0,
		code_score: lexical.code_score ?? lexical.bad_extention ?? 0,
		entropy: lexical.entropy ?? 0,
		symbol_ratio: lexical.symbol_ratio ?? 0,
		tag_count: lexical.tag_count ?? 0
	};
	const normalizedBehaviour = {
		...behaviour,
		base64: behaviour.base64 ?? Number(Boolean(parsedUrl.base64)),
		uses_ip: behaviour.uses_ip ?? address.is_ip ?? 0,
		long_subdomain: behaviour.long_subdomain ?? Number(Boolean(lexical.multi_subdomain || (lexical.subdomain_depth || 0) > 2))
	};
	const comments = report.comments || {};

	return {
		url_type: report.url_type === 'opac'
			? 'opaque'
			: report.url_type === 'hierarchical'
				? (scheme.toLowerCase() === 'https' ? 'secure_http' : 'plain_http')
				: report.url_type,
		parsed_url: parsedUrl,
		data: { lexical: normalizedLexical, behaviour: normalizedBehaviour },
		comments: {
			lexical: [...(comments.address || []), ...(comments.lexical || [])],
			behaviour: comments.behaviour || []
		},
		recommendation,
		specific_insights: report.specific_insights || '',
		_score: ml.status === 'ready' ? ml.score : null,
		ml_status: ml.status || 'unavailable',
		rule_signal_count: Number.isInteger(ml.risk_signal_count) ? ml.risk_signal_count : null,
		rule_signal_total: Number.isInteger(ml.risk_signal_total) ? ml.risk_signal_total : null,
		rule_score_percent: Number.isFinite(ml.rule_score_percent) ? ml.rule_score_percent : null,
		ml_message: ml.message || '',
		ml_error: ml.error || null,
		ml_verdict: ml.verdict || null
	};
}

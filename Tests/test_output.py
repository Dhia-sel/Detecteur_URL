import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from App.Core.pipeline import URLAnalyzerPipeline

# Test URL
test_url = "data:text/html;base64,PGh0bWw+PHNjcmlwdD5hbGVydCgnWW91IGhhdmUgYmVlbiBoYWNrZWQnKTs8L3NjcmlwdD48L2h0bWw+"

pipeline = URLAnalyzerPipeline(test_url)
result = pipeline.run()

if result["success"]:
    print("Analysis Report:")
    import json
    print(json.dumps(result["report"], indent=2))
else:
    print(f"Error: {result['error']}")
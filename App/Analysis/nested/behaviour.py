class behaviour_N_analyzer:  
    trusted= ["google", "facebook", "linkedin", "twitter", "microsoft", "yahoo"]

    def __init__(self, parsed_data):
        self.wrapper=parsed_data.get("enveloppe", {})
        self.inner_url=parsed_data.get("vrai url", "").lower() 
        self.key=self.wrapper.get("clef", "")

    def analyze(self):
        wrapperhost=self.wrapper.get("hote", "").lower()
        wrapperscheme=self.wrapper.get("schéma", "").lower()
        trusted_wrapper=0
        for trusted in self.trusted:
            if trusted in wrapperhost:
                trusted_wrapper=1
                break
        downgrade=0
        if wrapperscheme=="https" and self.inner_url.startswith("http:"):
            downgrade=1
        is_external=1
        if wrapperhost in self.inner_url:
            is_external=0
        keys = ["url", "link", "target", "src", "dest", "u", "go"]
        standard= 1 if self.key in keys else 0
        starts_with_digit=0
        clean_inner=self.inner_url.replace("https://", "").replace("http://", "")
        if len(clean_inner) > 0 and clean_inner[0].isdigit():
            starts_with_digit=1
        return {
            "trusted_wrapper":trusted_wrapper,
            "downgrade":downgrade,
            "is_external":is_external,
            "key_standard": standard,
            "target_digit":starts_with_digit
        }
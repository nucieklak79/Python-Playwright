import time

class MockLLM:

    @staticmethod
    def guess_new_locator(html_content: str, element_description: str) -> str:
        print(f"[Mock LLM] I received a DOM ({len(html_content)} characters).")
        print(f"[Mock LLM] I am looking for the element: '{element_description}'...")
       
        time.sleep(1) 

        if "login button" in element_description:
            print("[Mock LLM] I found a similar element! Returning selector: '#login-button'")
            return "#login-button"
            
        return ""
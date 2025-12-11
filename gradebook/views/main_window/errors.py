class InvalidTabError(Exception):
    def __init__(self, tab_name: str) -> None:
        """
        Error used if a tab name is invalid
        """
        super().__init__(f"Invalid tab name: {tab_name}")

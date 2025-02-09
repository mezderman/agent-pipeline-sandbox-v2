class Memory:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Memory, cls).__new__(cls)
            cls._instance.messages = []
        return cls._instance

    def add_message(self, message):
        """Add a message to memory."""
        self.messages.append(message)

    def get_messages(self):
        """Retrieve all messages from memory."""
        return self.messages
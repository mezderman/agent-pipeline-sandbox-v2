class ToolRegistry:
    _instance = None
    _tools = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def register_tool(self, name, func):
        self._tools[name] = func
    
    def get_tool(self, name):
        return self._tools.get(name) 
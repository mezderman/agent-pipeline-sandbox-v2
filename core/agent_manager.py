import json

class AgentManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AgentManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, agent_mapping=None):
        if not hasattr(self, 'initialized'):
            self.agents = {}
            self.initialized = True
            self.agents_path = []
            self.agent_mapping = agent_mapping

    @classmethod
    def get_instance(cls, agent_mapping=None):
        if cls._instance is None:
            cls._instance = cls(agent_mapping=agent_mapping)
        return cls._instance

    def register_agent(self, agent):
        """Register a agent using its name as the key"""
        self.agents[agent.get_name()] = agent
        return self.agents

    def get_agent(self, name):
        """Get a agent by name"""
        return self.agents.get(name)
    
    def run_agent(self, name, data, visited_agents=None):
        """Executes a specified agent."""
        if visited_agents is None:
            visited_agents = set()
            
        if name in visited_agents:
            print(f"Warning: Detected agent loop at {name}, stopping recursion")
            return data
            
        visited_agents.add(name)
        
        agent = self.agents.get(name)
        if agent:
            self.save_agent_path(agent)
            results = agent.run(data)
            print(f"Results: {results}")
            
            if hasattr(results, 'event') or (isinstance(results, dict) and 'event' in results):
                # Get the event and remove it from results
                event = results.event if hasattr(results, 'event') else results['event']
                if isinstance(results, dict):
                    results.pop('event', None)  # Remove event from dict
                elif hasattr(results, 'event'):
                    delattr(results, 'event')  # Remove event from object
                    
                if event in self.agent_mapping:
                    agent_name = self.agent_mapping[event]
                    results = self.run_agent(agent_name, results, visited_agents)
            return results
        else:
            raise ValueError(f"agent {name} not found")
        
    def save_agent_path(self, agent):
        self.agents_path.append(agent)
        return self.agents_path
    
    def get_agents_path(self):
        return self.agents_path
    
    def get_agents_data_logger(self):
        agent_logs = []
        
        for agent in self.agents_path:
            agent_data = {
                "agent_name": agent.get_name(),
                "nodes_data": []
            }
            
            for node in agent.nodes:
                node_output = node.get_output_data() if hasattr(node, 'get_output_data') else None
                if node_output:  # Only add nodes that have data
                    node_data = {
                        "node_name": node.get_name(),
                        "output_data": node_output
                    }
                    agent_data["nodes_data"].append(node_data)
            
            if agent_data["nodes_data"]:  # Only add agents that have nodes with data
                agent_logs.append(agent_data)
        
        return agent_logs
    
    def get_agents_data_logger_json(self):
        logs = self.get_agents_data_logger()
        formatted_logs = json.dumps(logs, indent=2, cls=self.CustomJSONEncoder)
        return formatted_logs
    
    class CustomJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            # Handle specific custom objects
            if hasattr(obj, '__dict__'):
                return obj.__dict__
            try:
                # Try to convert the object to a dict
                return vars(obj)
            except:
                # If all else fails, try string representation
                return str(obj)


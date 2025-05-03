class BaseComponent:
    
    # Method to be overridden by subclasses
    def build_component(self, entity_id, model, **kwargs):
        raise NotImplementedError
    
    def outer_div(self, component):
        return component

    def component_data(self, entity_id, model):
        raise NotImplementedError

    def __call__(self, entity_id, model, **kwargs):
        # Ensure kwargs are passed to build_component
        component = self.build_component(entity_id, model, **kwargs)
        return self.outer_div(component)

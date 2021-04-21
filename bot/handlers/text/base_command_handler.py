class BaseCommandHandler():
    def __init__(self, analytic_id: str):
        self.analytic_id = analytic_id
        
    async def handle(self, *args, **kwargs):
        ...
    
    async def __call__(self, *args, **kwargs):
        return await self.handle(*args, **kwargs)

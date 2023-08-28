ALL_TOOLS = []

class Tool:
    def __init__(self, name, func, description):
        self.name = name
        self.func = func
        self.description = description
        ALL_TOOLS.append(self)

class SerpAPIWrapper:
    def run(self):
        return "some data"


def fake_func(inp: str) -> str:
    return "foo"


# Create Search tool and automatically add it to ALL_TOOLS
search = SerpAPIWrapper()
Tool(
    name="Search",
    func=search.run,
    description="useful for when you need to answer questions about current events",
)

# Create fake tools and automatically add them to ALL_TOOLS
for i in range(99):
    Tool(
        name=f"foo-{i}",
        func=fake_func,
        description=f"a silly function that you can use to get more information about the number {i}",
    )

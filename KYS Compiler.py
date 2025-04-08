import re
import ast

memory = {}

def memeory_checker() -> None:
    for key in memory.keys():
        if type(memory[key]) != function:
            raise Exception(f"'{key}' is not a function.")

create = lambda name, value: memory.update({name: value})
get = lambda name: memory.get(name, None)
set = lambda name, value: memory.update({name: value})
delete = lambda name: memory.pop(name, None)
call = lambda func, *args: func(*args)
ternary = lambda condition, true_value, false_value: true_value() if condition() else false_value()
def loop(looping:function, condition:function) -> None:
    while condition():
        looping()
print = lambda text: print(text)
ask = lambda: input()


set("create", create)
set("get", get)
set("set", set)
set("delete", delete)
set("call", call)
set("ternary", ternary)
set("loop", loop)

def removeCurlyBraces(code):
    block_counter = 0
    lines = code.split('\n')
    result = []
    stack = []  # Keeps track of open block info: (indent, variable name, block id)
    current_block = []

    def flush_block(indent, varname, block_lines, block_id):
        func_name = f"__block_{block_id}"
        func_def = [f"{' ' * indent}def {func_name}():"] + \
                    [f"{' ' * (indent + 4)}{line}" for line in block_lines]
        assign = f"{' ' * indent}{varname} = {func_name}"
        return func_def + [assign]

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Detect a line like: name = {
        match = re.match(r"(\w+)\s*=\s*{\s*$", stripped)
        if match:
            varname = match.group(1)
            indent = len(line) - len(line.lstrip())
            block_id = block_counter
            block_counter += 1
            stack.append((indent, varname, block_id))
            current_block.append([])  # Start a new block
            i += 1
            continue

        elif stripped == "}":
            if not stack:
                raise SyntaxError("Unexpected }")
            indent, varname, block_id = stack.pop()
            block_lines = current_block.pop()
            result += flush_block(indent, varname, block_lines, block_id)
            i += 1
            continue

        elif stack:
            current_block[-1].append(line)
            i += 1
        else:
            result.append(line)
            i += 1

    if stack:
        raise SyntaxError("Unclosed block")

    return '\n'.join(result)

# Example usage:
if __name__ == "__main__":
    source = """
x = {
    print("Hello")
    print("World")
}

y = {
    a = 1
    b = 2
    print(a + b)
}

print("Done")
print(call(x))
print(call(y))
"""
    output = removeCurlyBraces(source)
    exec(output)

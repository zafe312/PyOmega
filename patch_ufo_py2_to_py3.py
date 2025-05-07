import os

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = content.replace('.iteritems()', '.items()')
    content = content.replace('.itervalues()', '.values()')
    content = content.replace('.iterkeys()', '.keys()')
    content = content.replace('xrange(', 'range(')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched: {filepath}")

def patch_ufo_model(ufo_path):
    if not os.path.isdir(ufo_path):
        print(f"Error: {ufo_path} is not a directory.")
        return

    print(f"Patching UFO model at: {ufo_path}")
    for filename in os.listdir(ufo_path):
        if filename.endswith('.py'):
            patch_file(os.path.join(ufo_path, filename))

# Example usage:
if __name__ == "__main__":
    ufo_model_path = "Model/ScalarSingletDM_UFO"  # Change this to your model path
    patch_ufo_model(ufo_model_path)
import psutil

def check_capacity():
    memory_info = psutil.virtual_memory()
    print(f"Current CPU memory usage: {memory_info.percent}%")

if __name__ == "__main__":
    check_capacity()
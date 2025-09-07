# Main Memory (RAM)
RAM = [i * 5 for i in range(1, 21)]  # 20 words: 5, 10, ..., 100

# Page table: One-to-one mapping
PAGE_TABLE = {i: i for i in range(len(RAM))}

# TLB (Translation Lookaside Buffer) and Cache
TLB = {}
CACHE = {}
TLB_SIZE = 5
CACHE_SIZE = 5

# Stats counters
stats = {"tlb_hits": 0, "tlb_misses": 0, "cache_hits": 0, "cache_misses": 0}

# Simulator function
def read_from_virtual_address(virtual_address):
    print(f"\nReading virtual address: {virtual_address}")

    # --- Step 1: Check TLB ---
    if virtual_address in TLB:
        print("Translation Lookaside Buffer[TLB], hit!")
        physical_address = TLB[virtual_address]
        stats["tlb_hits"] += 1
    else:
        print("Translation Lookaside Buffer[TLB], miss!")
        stats["tlb_misses"] += 1
        # Lookup page table (always mapped here)
        physical_address = PAGE_TABLE[virtual_address]
        print("Page Table hit!")
        
        # Update TLB with FIFO replacement
        if len(TLB) >= TLB_SIZE:
            oldest = next(iter(TLB))
            del TLB[oldest]
        TLB[virtual_address] = physical_address

    # --- Step 2: Check Cache ---
    if physical_address in CACHE:
        print("Cache hit!")
        stats["cache_hits"] += 1
        data = CACHE[physical_address]
    else:
        print("Cache miss! Fetching data from RAM...")
        stats["cache_misses"] += 1
        data = RAM[physical_address]
        
        # Update Cache with FIFO replacement
        if len(CACHE) >= CACHE_SIZE:
            oldest = next(iter(CACHE))
            del CACHE[oldest]
        CACHE[physical_address] = data

    print(f"Data returned: {data}")
    return data

# ----------------- USER INPUT -----------------
if __name__ == "__main__":
    print("\nIMPLEMENTATION OF A MEMORY SYSTEM SIMULATOR WITH TLB, PAGE TABLE, CACHE AND MAIN MEMORY...  \nEnter virtual addresses (0-19). Type 'exit' to quit.")

    while True:
        user_input = input("\nEnter virtual address: ")
        if user_input.lower() == "exit":
            break
        if not user_input.isdigit():
            print("Please enter a valid number between 0 and 19.")
            continue
        va = int(user_input)
        if va < 0 or va >= len(RAM):
            print("Virtual address out of range. Enter 0-19.")
            continue
        read_from_virtual_address(va)

    # Print final statistics
    print("\n--- Simulation Stats ---")
    for k, v in stats.items():
        print(f"{k}: {v}")

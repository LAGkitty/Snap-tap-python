import keyboard
import time

# Define the key groups that should cancel each other out
key_groups = [
    {'a', 'd'},
    {'w', 's'}
]

# Track the currently active key
current_key = None

def get_active_group(key):
    for group in key_groups:
        if key in group:
            return group
    return None

def on_key_event(event):
    global current_key

    if event.event_type == keyboard.KEY_DOWN:
        if event.name in {'a', 'd', 'w', 's'}:
            new_key = event.name
            new_group = get_active_group(new_key)

            if new_group:
                # If a key is already active and belongs to the same group as the new key
                if current_key and current_key != new_key:
                    current_group = get_active_group(current_key)
                    if current_group == new_group:
                        keyboard.release(current_key)

                # Update to the new key and group
                current_key = new_key
                keyboard.press(new_key)
                
            elif current_key:
                # If no valid group, just release the current key if it's not the new key
                if current_key != new_key:
                    keyboard.release(current_key)
                    current_key = None

    elif event.event_type == keyboard.KEY_UP:
        if event.name == current_key:
            keyboard.release(current_key)
            current_key = None

            # Check if any other keys are pressed and belong to the same group
            for key in {'a', 'd', 'w', 's'}:
                if keyboard.is_pressed(key):
                    group = get_active_group(key)
                    if group and key in group:
                        current_key = key
                        keyboard.press(key)
                        break

# Set up listeners for the keys
keyboard.hook(on_key_event)

# Active event loop to keep the script running
try:
    print("Script is running. Press Ctrl+C to exit.")
    while True:
        time.sleep(0.1)  # Sleep for a short duration to reduce CPU usage
except KeyboardInterrupt:
    print("\nScript terminated.")

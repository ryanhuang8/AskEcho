# AskEcho

1. Copy to Mac Shell Script
- Replace `/usr/local/bin/python3` with your python path
- Put `explainer_elevenlabs.py` into the path `~/Code/AskEcho/explainer_elevenlabs.py`
```bash
#!/bin/bash
# Show notification
osascript -e 'display notification "Processing your request..." with title "Text Explainer"'

# Get the selected text
selected_text="$1"

# Log
echo "Script started at $(date)" >> /tmp/explainer_log.txt
echo "Selected text: $selected_text" >> /tmp/explainer_log.txt

# Call the Python script
/usr/local/bin/python3 ~/Code/AskEcho/explainer_elevenlabs.py "$selected_text" 2>> /tmp/explainer_log.txt

echo "Script finished at $(date)" >> /tmp/explainer_log.txt
```
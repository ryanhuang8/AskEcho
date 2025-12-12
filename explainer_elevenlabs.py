#!/usr/bin/env python3
import sys
import os
import webbrowser
import tempfile
from pathlib import Path
import json
import subprocess

def create_html(selected_text, agent_id, supabase_url, supabase_anon_key,
                firebase_api_key=None, firebase_auth_domain=None,
                firebase_project_id=None, firebase_database_url=None):
    """Create HTML file with ElevenLabs widget, Supabase links, and Firebase user lookup"""
    
    # Create dynamic variables object
    dynamic_vars = {
        "selected_text": selected_text
    }
    
    # Convert to JSON string for the HTML attribute
    dynamic_vars_json = json.dumps(dynamic_vars).replace("'", "&#39;")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ask Echo</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }}
        
        .header-left {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .header h1 {{
            color: #333;
            font-size: 16px;
            margin: 0;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            background: #e8f5e9;
            border: 1px solid #4caf50;
            border-radius: 12px;
            color: #2e7d32;
            font-size: 11px;
            font-weight: 600;
        }}
        
        .voice-selector {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .voice-label {{
            font-size: 12px;
            color: #666;
            font-weight: 600;
        }}
        
        .voice-dropdown {{
            padding: 6px 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 12px;
            background: white;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .voice-dropdown:hover {{
            border-color: #667eea;
        }}
        
        .voice-dropdown:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .selected-text {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 12px;
            font-size: 12px;
            color: #666;
            max-height: 80px;
            overflow-y: auto;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }}
        
        .selected-text-label {{
            font-size: 10px;
            color: #999;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        
        .content-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        .links-container {{
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .links-header {{
            color: white;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .links-title {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .refresh-button {{
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .refresh-button:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-1px);
        }}
        
        .refresh-button:active {{
            transform: translateY(0);
        }}
        
        .refresh-button.loading {{
            opacity: 0.6;
            cursor: wait;
        }}
        
        .links-status {{
            font-size: 11px;
            padding: 2px 8px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            font-weight: normal;
        }}
        
        .link-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 8px;
            padding: 12px;
            transition: all 0.2s ease;
            cursor: pointer;
            animation: slideIn 0.3s ease;
        }}
        
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateX(20px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        .link-card:hover {{
            transform: translateX(-4px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .link-url {{
            color: #667eea;
            font-size: 12px;
            text-decoration: none;
            word-break: break-all;
            display: block;
            font-weight: 500;
        }}
        
        .link-domain {{
            color: #999;
            font-size: 10px;
            margin-top: 4px;
        }}
        
        .no-links {{
            color: rgba(255, 255, 255, 0.7);
            font-size: 13px;
            text-align: center;
            padding: 40px 20px;
        }}
        
        .loading-spinner {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}

        /* Scrollbar styling */
        .links-container::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .links-container::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }}
        
        .links-container::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.3);
            border-radius: 4px;
        }}
        
        .links-container::-webkit-scrollbar-thumb:hover {{
            background: rgba(255, 255, 255, 0.5);
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-left">
            <h1>🎙️ Ask Echo</h1>
            <div class="status-badge">✓ Context Loaded</div>
        </div>
        <div class="voice-selector">
            <label class="voice-label" for="voiceSelect">Voice:</label>
            <select id="voiceSelect" class="voice-dropdown">
                <option value="21m00Tcm4TlvDq8ikWAM">Rachel (Default)</option>
                <option value="AZnzlk1XvdvUeBnXmlld">Domi</option>
                <option value="EXAVITQu4vr4xnSDxMaL">Bella</option>
                <option value="ErXwobaYiN019PkySvjV">Antoni</option>
                <option value="MF3mGyEYCl7XYWbV9V6O">Elli</option>
                <option value="TxGEqnHWrfWFTfGW9XjX">Josh</option>
                <option value="VR6AewLTigWG4xSOukaG">Arnold</option>
                <option value="pNInz6obpgDQGcFmaJgB">Adam</option>
                <option value="yoZ06aMxZJJ28mfd3POQ">Sam</option>
                <option value="CwhRBWXzGAHq8TQ4Fs17">Roger</option>
            </select>
        </div>
    </div>
    
    <div class="selected-text">
        <div class="selected-text-label">Selected Text</div>
        <div>{selected_text[:150]}{'...' if len(selected_text) > 150 else ''}</div>
    </div>
    
    <div class="content-container">
        <div class="links-container" id="linksContainer">
            <div class="links-header">
                <div class="links-title">
                    🔗 Research Links
                    <span class="links-status" id="linksStatus">
                        0 links
                    </span>
                </div>
                <button class="refresh-button" id="refreshButton">
                    🔄 Get Links
                </button>
            </div>
            <div class="no-links" id="noLinksMessage">
                Click "Get Links" to load research links from Echo
            </div>
        </div>
    </div>
    
    <elevenlabs-convai
        id="echoAgent"
        agent-id="{agent_id}"
        dynamic-variables='{dynamic_vars_json}'
        override-voice-id="21m00Tcm4TlvDq8ikWAM"
    ></elevenlabs-convai>
    
    <script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <!-- Firebase SDKs -->
    <script src="https://www.gstatic.com/firebasejs/10.7.2/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.2/firebase-firestore-compat.js"></script>
    
    <script>
        // Handle voice selection
        const voiceSelect = document.getElementById('voiceSelect');
        const echoAgent = document.getElementById('echoAgent');
        
        voiceSelect.addEventListener('change', (e) => {{
            const selectedVoice = e.target.value;
            console.log('Voice changed to:', selectedVoice);
            
            // Update the agent's voice
            echoAgent.setAttribute('override-voice-id', selectedVoice);
            
            // Show confirmation
            const statusBadge = document.querySelector('.status-badge');
            const originalText = statusBadge.textContent;
            statusBadge.textContent = '✓ Voice Updated';
            statusBadge.style.background = '#e3f2fd';
            statusBadge.style.borderColor = '#2196f3';
            statusBadge.style.color = '#1565c0';
            
            setTimeout(() => {{
                statusBadge.textContent = originalText;
                statusBadge.style.background = '#e8f5e9';
                statusBadge.style.borderColor = '#4caf50';
                statusBadge.style.color = '#2e7d32';
            }}, 2000);
        }});
    </script>
    
    <script>
        const SUPABASE_URL = '{supabase_url}';
        const SUPABASE_ANON_KEY = '{supabase_anon_key}';
        
        const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        
        const linksContainer = document.getElementById('linksContainer');
        const linksStatus = document.getElementById('linksStatus');
        const noLinksMessage = document.getElementById('noLinksMessage');
        const refreshButton = document.getElementById('refreshButton');
        
        let displayedLinks = new Set();
        let isLoading = false;
        
        function extractDomain(url) {{
            try {{
                const urlObj = new URL(url);
                return urlObj.hostname.replace('www.', '');
            }} catch (e) {{
                return 'Unknown domain';
            }}
        }}
        
        function displayLinks(links) {{
            if (!links || links.length === 0) return;
            
            // Hide "no links" message
            if (noLinksMessage) {{
                noLinksMessage.style.display = 'none';
            }}
            
            links.forEach(url => {{
                // Skip if already displayed
                if (displayedLinks.has(url)) {{
                    console.log(`Skipping duplicate link: ${{url}}`);
                    return;
                }}
                
                displayedLinks.add(url);
                console.log(`Adding new link: ${{url}}`);
                
                const linkCard = document.createElement('div');
                linkCard.className = 'link-card';
                linkCard.onclick = () => window.open(url, '_blank');
                
                const domain = extractDomain(url);
                
                linkCard.innerHTML = `
                    <a href="${{url}}" target="_blank" class="link-url" onclick="event.stopPropagation()">
                        ${{url}}
                    </a>
                    <div class="link-domain">${{domain}}</div>
                `;
                
                linksContainer.appendChild(linkCard);
            }});
            
            // Update status
            linksStatus.textContent = `${{displayedLinks.size}} links`;
        }}
        
        function clearAllLinks() {{
            // Remove all link cards
            const linkCards = document.querySelectorAll('.link-card');
            linkCards.forEach(card => card.remove());
            
            // Clear the set
            displayedLinks.clear();
            
            // Show "no links" message
            if (noLinksMessage) {{
                noLinksMessage.style.display = 'block';
            }}
            
            // Update status
            linksStatus.textContent = '0 links';
            
            console.log('Cleared all links');
        }}
        
        async function fetchLinks() {{
            if (isLoading) return;
            
            isLoading = true;
            refreshButton.classList.add('loading');
            refreshButton.textContent = '⏳ Loading...';
            
            console.log('=== FETCHING LINKS ===');
            
            // Clear existing links before fetching new ones
            clearAllLinks();
            
            try {{
                const {{ data, error }} = await supabase
                    .from('test')
                    .select('*')
                    .limit(10);
                
                console.log('Fetch result - data:', data);
                console.log('Fetch result - error:', error);
                
                if (error) {{
                    console.error('Error fetching links:', error);
                    linksStatus.textContent = '⚠️ Error';
                    return;
                }}
                
                if (data && data.length > 0) {{
                    console.log(`Processing ${{data.length}} rows`);
                    data.forEach((row, index) => {{
                        console.log(`Row ${{index}}:`, row);
                        
                        if (row.links) {{
                            let linksData = row.links;
                            console.log(`Row ${{index}} links (raw):`, linksData);
                            console.log(`Row ${{index}} links type:`, typeof linksData);
                            
                            if (typeof linksData === 'string') {{
                                try {{
                                    linksData = JSON.parse(linksData);
                                    console.log(`Row ${{index}} links (parsed):`, linksData);
                                }} catch (e) {{
                                    console.error('Error parsing links string:', e);
                                    return;
                                }}
                            }}
                            
                            if (linksData && linksData.website_links && Array.isArray(linksData.website_links)) {{
                                console.log(`Row ${{index}} has ${{linksData.website_links.length}} website links`);
                                linksData.website_links.forEach((link, i) => {{
                                    console.log(`  Link ${{i}}: ${{link}}`);
                                }});
                                displayLinks(linksData.website_links);
                            }} else {{
                                console.log(`Row ${{index}} - no valid website_links array found`);
                            }}
                        }} else {{
                            console.log(`Row ${{index}} has no links column`);
                        }}
                    }});
                }} else {{
                    console.log('No data returned from query');
                }}
                
                console.log('After processing - displayed links count:', displayedLinks.size);
                linksStatus.textContent = `${{displayedLinks.size}} links`;
            }} catch (error) {{
                console.error('Error in fetchLinks:', error);
                linksStatus.textContent = '⚠️ Error';
            }} finally {{
                isLoading = false;
                refreshButton.classList.remove('loading');
                refreshButton.textContent = '🔄 Get Links';
                console.log('=== FETCH COMPLETE ===');
            }}
        }}
        
        async function subscribeToLinks() {{
            try {{
                console.log('Ready to fetch links on demand');
                
                // Add click handler to refresh button
                refreshButton.addEventListener('click', fetchLinks);
                
            }} catch (error) {{
                console.error('Error setting up link fetcher:', error);
            }}
        }}
        
        // Initialize when page loads
        window.addEventListener('load', () => {{
            subscribeToLinks();
        }});
    </script>

    <!-- Firebase Users Lookup -->
    <script>
        const FIREBASE_CONFIG = {{
            apiKey: '{firebase_api_key or ''}',
            authDomain: '{firebase_auth_domain or ''}',
            projectId: '{firebase_project_id or ''}',
            databaseURL: '{firebase_database_url or ''}',
        }};

        const hasFirebase = FIREBASE_CONFIG.apiKey && FIREBASE_CONFIG.projectId;

        function ensureFirebase() {{
            if (!hasFirebase) return null;
            try {{
                const app = firebase.apps && firebase.apps.length ? firebase.app() : firebase.initializeApp(FIREBASE_CONFIG);
                return firebase.firestore();
            }} catch (e) {{
                console.error('Firebase init error:', e);
                return null;
            }}
        }}

        function renderUserSection() {{
            const container = document.querySelector('.content-container');
            const section = document.createElement('div');
            section.style.padding = '16px';
            section.style.background = 'rgba(255,255,255,0.95)';
            section.style.backdropFilter = 'blur(10px)';
            section.style.borderTop = '1px solid rgba(0,0,0,0.1)';

            section.innerHTML = `
                <div id="userResult" style="font-size:13px; color:#333; padding-top:2px;"></div>
            `;
            container.appendChild(section);

            const userResult = section.querySelector('#userResult');

            async function loadUsers() {{
                const db = ensureFirebase();
                if (!db) {{
                    document.body.innerHTML = `<div style="display:flex; align-items:center; justify-content:center; height:100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"><div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); padding: 14px 18px; border-radius: 10px; font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif; color:#333; font-size:14px; font-weight:600;">log into dashboard to use</div></div>`;
                    return;
                }}
                userResult.textContent = '';

                try {{
                    // Firestore: get all docs in 'users'
                    const snapshot = await db.collection('users').get();
                    const total = snapshot.size;

                    if (!total) {{
                        document.body.innerHTML = `<div style="display:flex; align-items:center; justify-content:center; height:100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"><div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); padding: 14px 18px; border-radius: 10px; font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif; color:#333; font-size:14px; font-weight:600;">log into dashboard to use</div></div>`;
                        return;
                    }}

                    const firstDoc = snapshot.docs[0];
                    const firstData = firstDoc.data() || {{}};

                    const firstName = firstData.firstName || firstData.firstname || (firstData.name ? firstData.name.split(' ')[0] : '');
                    const lastName = firstData.lastName || firstData.lastname || (firstData.name ? firstData.name.split(' ').slice(1).join(' ') : '');
                    if (firstName || lastName) {{
                        userResult.textContent = `User: ${{firstName}} ${{lastName}}`.trim();
                    }} else {{
                        userResult.textContent = '';
                    }}
                }} catch (e) {{
                    console.error('User lookup error:', e);
                    document.body.innerHTML = `<div style="display:flex; align-items:center; justify-content:center; height:100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"><div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); padding: 14px 18px; border-radius: 10px; font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif; color:#333; font-size:14px; font-weight:600;">log into dashboard to use</div></div>`;
                }}
            }}
            // Automatically load on page render
            loadUsers();
        }}

        window.addEventListener('load', () => {{
            renderUserSection();
        }});
    </script>
</body>
</html>"""
    
    return html_content

def open_popup_window(html_file):
    """Open HTML file in a small standalone window in background"""
    
    # Window dimensions - CHANGE THESE to resize the window
    width = 500
    height = 700
    x_position = 100
    y_position = 100
    
    # Try AppleScript with Chrome in background (doesn't steal focus)
    if sys.platform == 'darwin':
        try:
            # Calculate bounds: {left, top, right, bottom}
            # Note: Using 'make new window' WITHOUT 'activate' keeps Chrome in background
            applescript = f'''
            tell application "Google Chrome"
                set newWindow to make new window
                set bounds of newWindow to {{{x_position}, {y_position}, {x_position + width}, {y_position + height}}}
                set URL of active tab of newWindow to "file://{html_file}"
            end tell
            '''
            subprocess.run(['osascript', '-e', applescript], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            print(f"Opened Chrome window in background ({width}x{height})", file=sys.stderr)
            return
        except subprocess.CalledProcessError as e:
            print(f"AppleScript failed (Chrome might not be installed): {e}", file=sys.stderr)
            print("Trying fallback methods...", file=sys.stderr)
        except Exception as e:
            print(f"AppleScript error: {e}", file=sys.stderr)
            print("Trying fallback methods...", file=sys.stderr)
    
    # Fallback: Try Chrome with app mode
    chrome_paths = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Chromium.app/Contents/MacOS/Chromium',
        '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
    ]
    
    for chrome_path in chrome_paths:
        if os.path.exists(chrome_path):
            try:
                subprocess.Popen([
                    chrome_path,
                    f'--app=file://{html_file}',
                    f'--window-size={width},{height}',
                    f'--window-position={x_position},{y_position}',
                    '--new-window'
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"Opened with Chrome app mode", file=sys.stderr)
                return
            except Exception as e:
                print(f"Failed to open with {chrome_path}: {e}", file=sys.stderr)
                pass
    
    # Fallback: Try Firefox
    firefox_paths = [
        '/Applications/Firefox.app/Contents/MacOS/firefox',
    ]
    
    for firefox_path in firefox_paths:
        if os.path.exists(firefox_path):
            try:
                subprocess.Popen([
                    firefox_path,
                    '--new-window',
                    f'file://{html_file}'
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"Opened with Firefox", file=sys.stderr)
                return
            except Exception as e:
                print(f"Failed to open with Firefox: {e}", file=sys.stderr)
                pass
    
    # Final fallback: regular browser (will open full app)
    print("Warning: No Chrome/Firefox found. Using default browser (may open full app)", file=sys.stderr)
    webbrowser.open(f"file://{html_file}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get credentials from environment
    AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
    FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL")
    
    if not AGENT_ID:
        print("Error: ELEVENLABS_AGENT_ID not found in .env file", file=sys.stderr)
        print("Get your agent ID from: https://elevenlabs.io/app/conversational-ai", file=sys.stderr)
        sys.exit(1)
    
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        print("Error: SUPABASE_URL and SUPABASE_ANON_KEY not found in .env file", file=sys.stderr)
        print("Get these from your Supabase project settings", file=sys.stderr)
        sys.exit(1)
    
    # Get selected text
    if len(sys.argv) > 1:
        selected_text = sys.argv[1]
    else:
        selected_text = "No text selected"
    
    # Create temporary HTML file
    temp_dir = tempfile.gettempdir()
    html_file = Path(temp_dir) / "elevenlabs_assistant.html"
    
    # Write HTML
    html_content = create_html(
        selected_text,
        AGENT_ID,
        SUPABASE_URL,
        SUPABASE_ANON_KEY,
        firebase_api_key=FIREBASE_API_KEY,
        firebase_auth_domain=FIREBASE_AUTH_DOMAIN,
        firebase_project_id=FIREBASE_PROJECT_ID,
        firebase_database_url=FIREBASE_DATABASE_URL,
    )
    html_file.write_text(html_content)
    
    print(f"Opening popup window...", file=sys.stderr)
    print(f"HTML file: {html_file}", file=sys.stderr)
    
    # Open in popup window
    open_popup_window(html_file)
import streamlit as st

st.set_page_config(
    page_title="Don't Panic! — The Hitchhiker's Guide Engine",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Retro CRT Style ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    html, body, [class*="css"], .stMarkdown {
        font-family: 'Share Tech Mono', monospace !important;
    }

    .main {
        background-color: #0d1117;
    }

    .stChatMessage {
        background-color: #161b22;
        border-left: 3px solid #39FF14;
        border-radius: 4px;
        margin-bottom: 8px;
    }

    .crt-screen {
        background: #051408;
        border: 2px solid #39FF14;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 0 15px rgba(57, 255, 20, 0.2);
        color: #39FF14;
        margin-bottom: 20px;
    }

    .crt-title {
        font-size: 1.4rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 1px dashed #39FF14;
        padding-bottom: 6px;
        margin-bottom: 12px;
    }

    .badge {
        display: inline-block;
        padding: 2px 8px;
        margin: 2px;
        border-radius: 3px;
        border: 1px solid #39FF14;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Game Engine Initialization ---
def init_game():
    st.session_state.inventory = []
    st.session_state.current_location = "bedroom"
    st.session_state.bulldozer_stopped = False
    st.session_state.turns = 0
    st.session_state.history = [
        {"role": "assistant", "content": "You wake up with a skull-splitting headache. The room is spinning. You need your towel."}
    ]
    st.session_state.rooms = {
        "bedroom": {
            "name": "Arthur's Bedroom",
            "desc": "The morning sun blazes through your curtains like an unwelcome laser. Your dependable towel is draped over a nearby chair. Outside, an ominous rumbling sound vibrates the floorboards.",
            "items": ["towel"],
            "exits": {"south": "front_yard"},
        },
        "front_yard": {
            "name": "Country Cottage Front Yard",
            "desc": "A monstrous yellow bulldozer sits idling loudly in the morning dew, poised to demolish your cottage to make way for a bypass. Mr. L. Prosser sits atop it, looking mildly regretful but firm.",
            "items": [],
            "exits": {"north": "bedroom", "east": "pub"},
        },
        "pub": {
            "name": "The Horse & Groom Pub",
            "desc": "Ford Prefect sits in the corner nursing a pint of bitter. Several freshly poured pints of beer and bags of roasted peanuts sit on the counter.",
            "items": ["beer", "peanuts"],
            "exits": {"west": "front_yard"},
        },
        "vogon_hold": {
            "name": "Vogon Constructor Fleet Hold",
            "desc": "A dark, rubbery chamber reeking of damp mattresses, sour bureaucracy, and unwashed Vogon guard uniforms. A glowing terminal flashes: 'DON'T PANIC'.",
            "items": ["guide"],
            "exits": {},
        },
    }

if "inventory" not in st.session_state:
    init_game()

# --- Core Action Logic ---
def execute_command(cmd: str):
    cmd = cmd.strip().lower()
    st.session_state.turns += 1
    room_data = st.session_state.rooms[st.session_state.current_location]

    # Command: Quit / Restart
    if cmd in ["restart", "reset"]:
        init_game()
        st.session_state.history.append({"role": "assistant", "content": "Engine rebooted. Back to reality."})
        return

    # Command: Movement
    for direction in ["north", "south", "east", "west"]:
        if cmd == direction or cmd == f"go {direction}":
            if direction in room_data["exits"]:
                # Puzzle Gate 1: Bulldozer Check
                if st.session_state.current_location == "front_yard" and direction == "east":
                    if not st.session_state.bulldozer_stopped:
                        st.session_state.history.append({
                            "role": "assistant",
                            "content": "You can't just stroll to the pub! The bulldozer will crush your cottage the second your back is turned!"
                        })
                        return

                st.session_state.current_location = room_data["exits"][direction]
                new_room = st.session_state.rooms[st.session_state.current_location]
                st.session_state.history.append({
                    "role": "assistant",
                    "content": f"You walk {direction} into **{new_room['name']}**.\n\n{new_room['desc']}"
                })
            else:
                st.session_state.history.append({"role": "assistant", "content": "You cannot go that way."})
            return

    # Command: Take Item
    if cmd.startswith("take ") or cmd.startswith("get "):
        item = cmd.split(" ", 1)[1].strip()
        if item in room_data["items"]:
            room_data["items"].remove(item)
            st.session_state.inventory.append(item)
            st.session_state.history.append({"role": "assistant", "content": f"Taken: **{item}**."})
        else:
            st.session_state.history.append({"role": "assistant", "content": f"There is no {item} here."})
        return

    # Command: Lie Down / Block Bulldozer
    if cmd in ["lie down", "lie down in mud", "block bulldozer", "lie in front of bulldozer"]:
        if st.session_state.current_location == "front_yard":
            if "towel" not in st.session_state.inventory:
                st.session_state.history.append({
                    "role": "assistant",
                    "content": "You lie down in the mud, but without your towel, you feel terribly cold, undignified, and exposed."
                })
            else:
                st.session_state.history.append({
                    "role": "assistant",
                    "content": "You sprawl out heroically in the freezing English mud directly in front of the yellow bulldozer. Mr. Prosser sighs, shuts down the engine, and rubs his temples. The bypass is temporarily delayed."
                })
            st.session_state.bulldozer_stopped = True
        else:
            st.session_state.history.append({"role": "assistant", "content": "You lie down on the floor for a bit. Nothing happens."})
        return

    # Command: Drink Beer
    if cmd in ["drink beer", "drink pint", "have beer"]:
        if "beer" in st.session_state.inventory:
            st.session_state.history.append({
                "role": "assistant",
                "content": (
                    "You swallow the warm bitter beer down in three massive gulps. "
                    "Ford looks at you grimly: *'Drink up. Muscle relaxant for matter transference.'*\n\n"
                    "**RUUUUUMBLE!**\n\n"
                    "The sky tears apart with deafening sirens. Massive yellow slabs of metal blot out the sun. "
                    "Earth is being vaporized to build a hyperspace bypass! Ford grabs your towel, aims his Sub-Etha thumb at the sky, and *ZAPS* both of you out of existence just before impact!"
                )
            })
            st.session_state.current_location = "vogon_hold"
            return
        else:
            st.session_state.history.append({"role": "assistant", "content": "You don't have any beer to drink."})
        return

    # Command: Consult Guide
    if cmd in ["consult guide", "read guide", "use guide", "open guide"]:
        if "guide" in st.session_state.inventory:
            st.session_state.history.append({
                "role": "assistant",
                "content": (
                    "**[ THE HITCHHIKER'S GUIDE TO THE GALAXY ]**\n\n"
                    "• **EARTH:** Mostly harmless.\n"
                    "• **TOWEL:** A towel is about the most massively useful thing an interstellar hitchhiker can have.\n"
                    "• **VOGONS:** They are one of the most unpleasant races in the Galaxy. Not actually evil, but bad-tempered, bureaucratic, and callous. They wouldn't lift a finger to save their own grandmothers without orders signed in triplicate."
                )
            })
        else:
            st.session_state.history.append({"role": "assistant", "content": "You don't have the Hitchhiker's Guide to consult."})
        return

    # Command: Look
    if cmd in ["look", "l"]:
        st.session_state.history.append({
            "role": "assistant",
            "content": f"**{room_data['name']}**\n\n{room_data['desc']}"
        })
        return

    # Unrecognized Command
    st.session_state.history.append({
        "role": "assistant",
        "content": f"The Sub-Etha terminal does not understand *'{cmd}'*. Try verbs like: `go <direction>`, `take <item>`, `lie down`, `drink beer`, `consult guide`, or `look`."
    })

# --- Sidebar Display ---
with st.sidebar:
    st.markdown("### 📡 SUB-ETHA SENSOR PACKET")
    st.metric("Turn Counter", st.session_state.turns)
    
    st.markdown("---")
    st.markdown("### 🎒 INVENTORY")
    if st.session_state.inventory:
        for item in st.session_state.inventory:
            st.markdown(f"<span class='badge'>📦 {item.upper()}</span>", unsafe_allow_html=True)
    else:
        st.caption("Your pockets are empty.")

    st.markdown("---")
    st.markdown("### 🧭 QUICK COMMANDS")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("North"):
            st.session_state.history.append({"role": "user", "content": "go north"})
            execute_command("go north")
            st.rerun()
        if st.button("West"):
            st.session_state.history.append({"role": "user", "content": "go west"})
            execute_command("go west")
            st.rerun()
    with col2:
        if st.button("South"):
            st.session_state.history.append({"role": "user", "content": "go south"})
            execute_command("go south")
            st.rerun()
        if st.button("East"):
            st.session_state.history.append({"role": "user", "content": "go east"})
            execute_command("go east")
            st.rerun()

    if st.button("Restart Mission", use_container_width=True):
        init_game()
        st.rerun()

# --- Main Game Terminal View ---
current_room = st.session_state.rooms[st.session_state.current_location]

st.markdown(
    f"""
    <div class="crt-screen">
        <div class="crt-title">📟 {current_room['name']}</div>
        <p>{current_room['desc']}</p>
        <p><strong>Visible Items:</strong> {', '.join(current_room['items']) if current_room['items'] else 'None'}</p>
        <p><strong>Available Exits:</strong> {', '.join(current_room['exits'].keys()) if current_room['exits'] else 'No visible exits (you are trapped!)'}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Scrollable Narrative Log ---
for msg in st.session_state.history[-8:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Command Parser Input ---
user_input = st.chat_input("Enter command (e.g., 'take towel', 'lie down', 'drink beer', 'look')...")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    execute_command(user_input)
    st.rerun()

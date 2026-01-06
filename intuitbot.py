"""
Inuit Luxury Footwear Chatbot - Complete User-Friendly Version
Built with Python & Streamlit

Installation:
pip install streamlit

Run:
streamlit run inuit_chatbot.py

Features:
- Beautiful, modern UI
- Interactive conversation flow
- Product recommendations
- Video integration
- Progress tracking
- Easy to customize
"""

import streamlit as st
from datetime import datetime
import time

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="Inuit Luxury Footwear",
    page_icon="👞",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== CUSTOM STYLING ==========
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #1e293b 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #d97706 0%, #b45309 100%);
        color: white;
        border: none;
        padding: 14px 20px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #b45309 0%, #92400e 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1.2rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        gap: 1rem;
        animation: slideIn 0.3s ease-out;
    }
    @keyframes slideIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    .bot-message {
        background-color: white;
        border: 2px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .user-message {
        background: linear-gradient(90deg, #d97706 0%, #b45309 100%);
        color: white;
        flex-direction: row-reverse;
        box-shadow: 0 2px 8px rgba(217,119,6,0.3);
    }
    
    /* Avatar styling */
    .avatar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .bot-avatar {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    }
    .user-avatar {
        background: linear-gradient(135deg, #334155 0%, #1e293b 100%);
    }
    
    /* Product cards */
    .product-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        margin: 10px 0;
        transition: all 0.3s;
    }
    .product-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        border-color: #d97706;
    }
    
    /* Progress steps */
    .progress-step {
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 10px;
        transition: all 0.3s;
        cursor: pointer;
    }
    .progress-step:hover {
        transform: translateX(5px);
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #cbd5e1;
        padding: 12px;
        font-size: 15px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #d97706;
        box-shadow: 0 0 0 3px rgba(217,119,6,0.1);
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        gap: 6px;
        padding: 10px;
    }
    .typing-dot {
        width: 10px;
        height: 10px;
        background-color: #94a3b8;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out;
    }
    .typing-dot:nth-child(1) {animation-delay: -0.32s;}
    .typing-dot:nth-child(2) {animation-delay: -0.16s;}
    @keyframes bounce {
        0%, 80%, 100% {transform: scale(0);}
        40% {transform: scale(1);}
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE INITIALIZATION ==========
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'user_choices' not in st.session_state:
    st.session_state.user_choices = {
        'shoe_type': '',
        'occasion': '',
        'size': ''
    }
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'show_typing' not in st.session_state:
    st.session_state.show_typing = False
if 'playing_video' not in st.session_state:
    st.session_state.playing_video = None

# ========== CONVERSATION FLOW ==========
STEPS = [
    {
        'id': 'welcome',
        'message': "Welcome to Inuit! 👋\n\nWe craft luxury footwear that blends timeless elegance with uncompromising comfort. From handcrafted leather boots to sophisticated sneakers, each pair tells a story of Italian craftsmanship.",
        'type': 'quick_replies',
        'options': ['✨ Tell me more', '👞 Show me shoes']
    },
    {
        'id': 'intro',
        'message': "Perfect! Let's find your ideal pair. What type of shoe are you looking for today?",
        'type': 'buttons',
        'options': [
            ('👞 Formal Shoes', 'formal'),
            ('👟 Sneakers', 'sneakers'),
            ('🥾 Boots', 'boots'),
            ('👡 Loafers', 'loafers')
        ]
    },
    {
        'id': 'occasion',
        'message': "Excellent choice! What occasion are you shopping for?",
        'type': 'buttons',
        'options': [
            ('💼 Work/Business', 'work'),
            ('🎉 Special Events', 'events'),
            ('🚶 Everyday Wear', 'casual'),
            ('🎁 Gift', 'gift')
        ]
    },
    {
        'id': 'size',
        'message': "Great! What's your shoe size? (US sizing)",
        'type': 'quick_replies',
        'options': ['7-8', '9-10', '11-12', "❓ I'm not sure"]
    },
    {
        'id': 'recommendations',
        'message': "✨ Based on your preferences, here are our top recommendations:",
        'type': 'carousel',
        'products': [
            {
                'name': 'Milano Executive',
                'price': '$450',
                'emoji': '👞',
                'desc': 'Italian leather, hand-stitched perfection',
                'features': '• Full-grain leather\n• Goodyear welt\n• Italian craftsmanship'
            },
            {
                'name': 'Urban Elite',
                'price': '$380',
                'emoji': '👟',
                'desc': 'Premium comfort meets modern design',
                'features': '• Memory foam insole\n• Breathable mesh\n• Lightweight construction'
            },
            {
                'name': 'Heritage Classic',
                'price': '$520',
                'emoji': '🥾',
                'desc': 'Timeless craftsmanship for generations',
                'features': '• Hand-waxed leather\n• Storm welt\n• Lifetime warranty'
            }
        ]
    },
    {
        'id': 'videos',
        'message': "🎥 Want to see how we craft perfection?\n\nHere's a behind-the-scenes look at our workshop:",
        'type': 'videos',
        'videos': [
            {
                'title': '🔪 Leather Selection Process',
                'duration': '2:15',
                'description': 'See how we handpick the finest Italian leather',
                'url': 'https://www.youtube.com/watch?v=ACFejrSb9Vg',
                'thumbnail': 'https://img.youtube.com/vi/ACFejrSb9Vg/hqdefault.jpg'
            },
            {
                'title': '✂️ Hand Stitching Craftsmanship',
                'duration': '3:40',
                'description': 'Watch master craftsmen at work',
                'url': 'https://www.youtube.com/watch?v=MFDo-dtr9mk',
                'thumbnail': 'https://img.youtube.com/vi/MFDo-dtr9mk/hqdefault.jpg'
            },
            {
                'title': '✅ Quality Inspection',
                'duration': '1:55',
                'description': 'Our rigorous quality standards',
                'url': 'https://www.youtube.com/watch?v=BEBGtL_Q1iE',
                'thumbnail': 'https://img.youtube.com/vi/BEBGtL_Q1iE/hqdefault.jpg'
            }
        ]
    },
    {
        'id': 'order',
        'message': "🎁 Ready to experience Inuit luxury?\n\nWe offer:\n• Free worldwide shipping\n• Premium packaging\n• 30-day returns\n• Lifetime warranty",
        'type': 'buttons',
        'options': [
            ('🛒 Place Order', 'order'),
            ('💬 Chat with Expert', 'expert'),
            ('📧 Email Details', 'email')
        ]
    },
    {
        'id': 'conclusion',
        'message': "✨ Thank you for choosing Inuit!\n\nYour order will arrive in 5-7 business days. We'll send tracking details to your email.\n\nEnjoy your luxury footwear! 👞",
        'type': 'quick_replies',
        'options': ['📦 Track Order', '👞 Browse More', '🏠 Main Menu']
    }
]

# ========== HELPER FUNCTIONS ==========

def add_message(sender, message, **kwargs):
    """Add a message to chat history"""
    st.session_state.chat_history.append({
        'sender': sender,
        'message': message,
        'timestamp': datetime.now(),
        **kwargs
    })

def display_message(msg):
    """Display a chat message with beautiful styling"""
    if msg['sender'] == 'bot':
        st.markdown(f"""
        <div class="chat-message bot-message">
            <div class="avatar bot-avatar">🤖</div>
            <div style="flex: 1;">
                <div style="color: #1e293b; font-size: 15px; line-height: 1.6; white-space: pre-line;">
                    {msg['message']}
                </div>
                <div style="color: #94a3b8; font-size: 11px; margin-top: 8px;">
                    {msg['timestamp'].strftime('%I:%M %p')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="avatar user-avatar">👤</div>
            <div style="flex: 1;">
                <div style="font-size: 15px; line-height: 1.6;">
                    {msg['message']}
                </div>
                <div style="color: rgba(255,255,255,0.7); font-size: 11px; margin-top: 8px;">
                    {msg['timestamp'].strftime('%I:%M %p')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_typing_indicator():
    """Display typing animation"""
    st.markdown("""
    <div class="chat-message bot-message" style="padding: 0.8rem 1.2rem;">
        <div class="avatar bot-avatar">🤖</div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def handle_choice(choice, display_text=None):
    """Handle user selection and progress to next step"""
    text = display_text if display_text else choice
    add_message('user', text)
    
    # Save user choices
    step = st.session_state.current_step
    if step == 1:
        st.session_state.user_choices['shoe_type'] = choice
    elif step == 2:
        st.session_state.user_choices['occasion'] = choice
    elif step == 3:
        st.session_state.user_choices['size'] = choice
    
    # Show typing indicator
    st.session_state.show_typing = True
    st.rerun()

def advance_conversation():
    """Move to next step in conversation"""
    if st.session_state.current_step < len(STEPS) - 1:
        time.sleep(0.8)  # Simulate bot thinking
        st.session_state.current_step += 1
        current_step_data = STEPS[st.session_state.current_step]
        add_message('bot', current_step_data['message'], step_data=current_step_data)
        st.session_state.show_typing = False
        st.rerun()

def reset_chat():
    """Reset the entire conversation"""
    st.session_state.chat_history = []
    st.session_state.current_step = 0
    st.session_state.user_choices = {'shoe_type': '', 'occasion': '', 'size': ''}
    st.session_state.initialized = False
    st.session_state.show_typing = False
    st.session_state.playing_video = None
    st.rerun()

# ========== MAIN APP ==========

# Initialize chat with welcome message
if not st.session_state.initialized:
    add_message('bot', STEPS[0]['message'], step_data=STEPS[0])
    st.session_state.initialized = True

# Header Section
st.markdown("""
<div style='text-align: center; padding: 2rem 0 1rem 0;'>
    <h1 style='color: white; font-size: 3rem; margin-bottom: 0.5rem; 
               text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
        👞 Inuit Luxury Footwear
    </h1>
    <p style='color: #cbd5e1; font-size: 1.1rem;'>
        Your Personal Shopping Assistant
    </p>
</div>
""", unsafe_allow_html=True)

# Main Layout: Chat (Left) + Sidebar (Right)
col_chat, col_sidebar = st.columns([2.5, 1])

# ========== CHAT SECTION ==========
with col_chat:
    st.markdown("### 💬 Chat with Our Assistant")
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        # Display all messages
        for msg in st.session_state.chat_history:
            display_message(msg)
            
            # Show interactive elements only for the last bot message
            if msg['sender'] == 'bot' and msg == st.session_state.chat_history[-1]:
                step_data = msg.get('step_data', {})
                
                # Quick Reply Buttons
                if step_data.get('type') == 'quick_replies':
                    cols = st.columns(len(step_data['options']))
                    for idx, option in enumerate(step_data['options']):
                        with cols[idx]:
                            if st.button(option, key=f"quick_{idx}"):
                                handle_choice(option)
                
                # Regular Buttons
                elif step_data.get('type') == 'buttons':
                    for idx, (label, value) in enumerate(step_data['options']):
                        if st.button(label, key=f"btn_{idx}"):
                            handle_choice(value, label)
                
                # Product Carousel
                elif step_data.get('type') == 'carousel':
                    for idx, product in enumerate(step_data['products']):
                        with st.container():
                            st.markdown(f"""
                            <div class="product-card">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                                    <div style="display: flex; gap: 15px; align-items: center;">
                                        <span style="font-size: 40px;">{product['emoji']}</span>
                                        <div>
                                            <div style="font-weight: 700; color: #1e293b; font-size: 18px;">
                                                {product['name']}
                                            </div>
                                            <div style="font-size: 13px; color: #64748b; margin-top: 4px;">
                                                {product['desc']}
                                            </div>
                                        </div>
                                    </div>
                                    <div style="font-weight: 800; color: #b45309; font-size: 22px;">
                                        {product['price']}
                                    </div>
                                </div>
                                <div style="font-size: 12px; color: #475569; margin-bottom: 10px; white-space: pre-line;">
                                    {product.get('features', '')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button(f"👁️ View Details", key=f"prod_view_{idx}"):
                                    handle_choice(f"view_{product['name']}", f"📋 View {product['name']} details")
                            with col2:
                                if st.button(f"🛒 Add to Cart", key=f"prod_cart_{idx}"):
                                    handle_choice(f"add_{product['name']}", f"🛒 Add {product['name']} to cart")
                            st.markdown("<br>", unsafe_allow_html=True)
                
                # Video Section
                elif step_data.get('type') == 'videos':
                    for idx, video in enumerate(step_data['videos']):
                        with st.container():
                            col_thumb, col_info = st.columns([1, 2])
                            
                            with col_thumb:
                                if 'thumbnail' in video:
                                    st.image(video['thumbnail'], use_container_width=True)
                            
                            with col_info:
                                st.markdown(f"""
                                <div style="padding: 5px;">
                                    <div style="font-weight: 600; color: #1e293b; font-size: 15px; margin-bottom: 5px;">
                                        {video['title']}
                                    </div>
                                    <div style="font-size: 13px; color: #64748b; margin-bottom: 5px;">
                                        {video.get('description', '')}
                                    </div>
                                    <div style="font-size: 12px; color: #94a3b8;">
                                        ⏱️ Duration: {video['duration']}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if st.button(f"▶️ Watch Now", key=f"vid_{idx}"):
                                    st.session_state.playing_video = idx
                                    st.rerun()
                            
                            # Show video player if this video is selected
                            if st.session_state.playing_video == idx:
                                if 'url' in video:
                                    st.video(video['url'])
                                    if st.button(f"❌ Close Video", key=f"close_vid_{idx}"):
                                        st.session_state.playing_video = None
                                        st.rerun()
                                else:
                                    st.info("🎬 Video coming soon!")
                            
                            st.markdown("---")
                    
                    # Add Skip Option after all videos
                    st.markdown("<br>", unsafe_allow_html=True)
                    col_skip1, col_skip2 = st.columns(2)
                    with col_skip1:
                        if st.button("⏭️ Skip Videos - Continue Shopping", key="skip_videos", use_container_width=True):
                            st.session_state.playing_video = None
                            handle_choice("skip_videos", "⏭️ Skip videos and continue")
                    with col_skip2:
                        if st.button("✅ Done Watching - Next Step", key="done_videos", use_container_width=True):
                            st.session_state.playing_video = None
                            handle_choice("done_watching", "✅ Finished watching videos")
        
        # Show typing indicator
        if st.session_state.show_typing:
            show_typing_indicator()
            advance_conversation()
    
    # Message Input Area
    st.markdown("---")
    col_input, col_send = st.columns([5, 1])
    
    with col_input:
        user_input = st.text_input(
            "Type your message...",
            key="user_input",
            placeholder="Ask me anything about our shoes...",
            label_visibility="collapsed"
        )
    
    with col_send:
        if st.button("📤 Send", use_container_width=True):
            if user_input.strip():
                add_message('user', user_input)
                time.sleep(0.5)
                add_message('bot', 
                    "🤔 I didn't quite catch that!\n\nWould you like to explore our collections, speak with an expert, or return to the main menu?",
                    step_data={
                        'type': 'quick_replies',
                        'options': ['🏠 Main Menu', '💬 Human Agent', '👞 Collections']
                    }
                )
                st.rerun()

# ========== SIDEBAR SECTION ==========
with col_sidebar:
    # Progress Tracker
    st.markdown("### 📊 Your Journey")
    
    for idx, step in enumerate(STEPS):
        if idx < st.session_state.current_step:
            icon = "✅"
            color = "#10b981"
            bg = "#d1fae5"
            border = "#10b981"
        elif idx == st.session_state.current_step:
            icon = "🔵"
            color = "#f59e0b"
            bg = "#fef3c7"
            border = "#f59e0b"
        else:
            icon = "⭕"
            color = "#94a3b8"
            bg = "#f1f5f9"
            border = "#cbd5e1"
        
        st.markdown(f"""
        <div class="progress-step" style="background-color: {bg}; border: 2px solid {border};">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 18px;">{icon}</span>
                <div>
                    <div style="font-weight: 600; color: #1e293b; font-size: 13px;">
                        Step {idx + 1}
                    </div>
                    <div style="font-size: 11px; color: #64748b;">
                        {step['id'].title()}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # User Selections Summary
    st.markdown("### 📝 Your Selections")
    st.markdown(f"""
    <div style="background: white; padding: 15px; border-radius: 10px; border: 2px solid #e2e8f0;">
        <div style="margin-bottom: 10px;">
            <strong style="color: #1e293b;">👞 Shoe Type:</strong><br>
            <span style="color: #64748b;">{st.session_state.user_choices['shoe_type'] or '❌ Not selected'}</span>
        </div>
        <div style="margin-bottom: 10px;">
            <strong style="color: #1e293b;">🎯 Occasion:</strong><br>
            <span style="color: #64748b;">{st.session_state.user_choices['occasion'] or '❌ Not selected'}</span>
        </div>
        <div>
            <strong style="color: #1e293b;">📏 Size:</strong><br>
            <span style="color: #64748b;">{st.session_state.user_choices['size'] or '❌ Not selected'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features Overview
    st.markdown("### ✨ Why Choose Inuit?")
    st.markdown("""
    <div style="background: white; padding: 15px; border-radius: 10px; border: 2px solid #e2e8f0;">
        <div style="margin-bottom: 8px;">
            <strong style="color: #b45309;">🤝 Warm Service</strong><br>
            <span style="font-size: 12px; color: #64748b;">Luxury tone with personal care</span>
        </div>
        <div style="margin-bottom: 8px;">
            <strong style="color: #b45309;">🎨 Rich Experience</strong><br>
            <span style="font-size: 12px; color: #64748b;">Interactive shopping journey</span>
        </div>
        <div style="margin-bottom: 8px;">
            <strong style="color: #b45309;">🛍️ Easy Navigation</strong><br>
            <span style="font-size: 12px; color: #64748b;">Simple, guided process</span>
        </div>
        <div>
            <strong style="color: #b45309;">✅ Quality Guarantee</strong><br>
            <span style="font-size: 12px; color: #64748b;">Premium Italian craftsmanship</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action Buttons
    if st.button("🔄 Restart Conversation", use_container_width=True):
        reset_chat()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Help Section
    st.markdown("### 💡 Need Help?")
    st.info("💬 Type your questions anytime or use the quick reply buttons for faster navigation!", icon="ℹ️")
    
    # Contact
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <div style="font-size: 12px; color: #cbd5e1;">
            📧 support@inuit.com<br>
            📞 1-800-INUIT-SHOES
        </div>
    </div>
    """, unsafe_allow_html=True)
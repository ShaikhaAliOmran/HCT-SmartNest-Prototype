"""HCT SmartNest: educational UI/UX prototype. Fictional records; no real authentication."""
from datetime import date, datetime
from io import StringIO
import csv
from pathlib import Path
import streamlit as st

st.set_page_config(page_title='HCT SmartNest | Prototype', page_icon='🏠', layout='wide')
LOGO = Path(__file__).parent / 'assets' / 'smartnest-logo.png'
SCREENS = ['Login', 'Staff Dashboard', 'Attendance', 'Child Profile', 'Parent View', 'Consent', 'Messages', 'Search', 'Reports', 'Notifications', 'Pre-enrollment']
FR = {'Login':'FR01', 'Staff Dashboard':'FR05, FR07', 'Attendance':'FR05', 'Child Profile':'FR03, FR04', 'Parent View':'FR06, FR07', 'Consent':'FR15', 'Messages':'FR13', 'Search':'FR17', 'Reports':'FR11', 'Notifications':'FR09', 'Pre-enrollment':'FR14'}
ROLES = {'Staff': ['Login','Staff Dashboard','Attendance','Child Profile','Messages','Search','Reports','Notifications','Pre-enrollment'], 'Parent':['Login','Parent View','Messages','Notifications','Pre-enrollment'], 'Administrator': SCREENS, 'Prospective parent':['Login','Pre-enrollment']}

st.markdown("""
<style>
/* HCT SmartNest brand palette */
:root { --nest-blue:#202D91; --nest-pink:#C65C7B; --nest-gold:#F0BF50; }
.stApp, [data-testid="stAppViewContainer"] {background:#F7F8FF; color:#202D4A;}
[data-testid="stMain"] h1, [data-testid="stMain"] h2,
[data-testid="stMain"] h3 {color:#202D4A; letter-spacing:-.02em;}
/* Left sidebar */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
  background:#202D91 !important;
}
[data-testid="stSidebar"] {border-right:1px solid #192477;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] label, [data-testid="stSidebar"] label p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
  color:#FFFFFF !important;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {opacity:.85;}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  border-radius:8px; padding:5px 9px; margin:2px 0;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
  background:#3947A7;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
  color:#FFFFFF !important; font-weight:650;
}
[data-testid="stSidebar"] [data-testid="stRadio"] input {accent-color:#C65C7B;}
[data-testid="stSidebar"] hr {border-color:#7B85C1;}
/* Keep the demo-role selector readable */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background:#FFFFFF !important; border:1px solid #D8DDED;
}
[data-testid="stSidebar"] [data-baseweb="select"] * {color:#202D4A !important;}
/* Forms, tables, and inputs */
[data-testid="stMetric"], [data-testid="stForm"] {
  background:#FFFFFF; border:1px solid #E1E5F0;
  border-radius:10px; padding:16px;
}
[data-testid="stDataFrame"] {border-radius:8px; overflow:hidden;}
[data-testid="stMain"] input, [data-testid="stMain"] textarea {
  background:#FFFFFF; color:#202D4A;
}
[data-testid="stMain"] div.stButton > button[kind="primary"],
[data-testid="stMain"] button[data-testid="stFormSubmitButton-primary"] {
  background:#202D91; color:white; border-color:#202D91; border-radius:7px;
}
[data-testid="stMain"] div.stButton > button[kind="primary"]:hover {
  background:#3443A3;
}
.prototype-note {
  padding:11px 15px; background:#FFF8E7; color:#544A31;
  border-left:4px solid #F0BF50; border-radius:5px;
  margin:12px 0 22px;
}
.small-note {color:#66738A;font-size:.9rem;}
</style>
""", unsafe_allow_html=True)

if 'role' not in st.session_state: st.session_state.role = 'Staff'
if 'page' not in st.session_state: st.session_state.page = 'Login'
if 'children' not in st.session_state:
    st.session_state.children = [
        {'id':'SN-001','name':'Aisha M.','class':'Blue Room','status':'Present','in':'08:04','out':'','allergy':'None recorded','contact':'050-XXX-0101'},
        {'id':'SN-002','name':'Omar H.','class':'Blue Room','status':'Present','in':'08:12','out':'','allergy':'Peanuts (demo)','contact':'050-XXX-0102'},
        {'id':'SN-003','name':'Noor A.','class':'Yellow Room','status':'Absent','in':'','out':'','allergy':'None recorded','contact':'050-XXX-0103'},
        {'id':'SN-004','name':'Salem K.','class':'Yellow Room','status':'Present','in':'08:21','out':'','allergy':'None recorded','contact':'050-XXX-0104'},
    ]
if 'messages' not in st.session_state: st.session_state.messages = [{'From':'Nursery staff','To':'Parent','Message':'Reminder: Please bring a spare change of clothes.'}]
if 'notices' not in st.session_state: st.session_state.notices = ['Nursery will share the weekly activity summary on Thursday.', 'Please review authorized pickup details when they change.']
if 'consents' not in st.session_state: st.session_state.consents = {}
if 'updates' not in st.session_state: st.session_state.updates = ['Outdoor play and story time completed.', 'Lunch and rest time updates will be shared by staff.']

with st.sidebar:
    st.image(str(LOGO), width=150)
    st.caption('HCT SmartNest · UI/UX prototype')
    role = st.selectbox('Demo user', list(ROLES), index=list(ROLES).index(st.session_state.role))
    if role != st.session_state.role:
        st.session_state.role = role
        st.session_state.page = 'Login'
        st.rerun()
    choices = ROLES[role]
    current = st.session_state.page if st.session_state.page in choices else choices[0]
    page = st.radio('Navigation', choices, index=choices.index(current))
    st.session_state.page = page
    st.divider()
    st.caption('All records are fictional. Role switching is for demonstration only.')

st.title(page)
st.caption(f'Actor: {role}  |  Requirement: {FR[page]}  |  Usability: NFR03')
st.markdown('<div class="prototype-note">DEMO PROTOTYPE — not connected to a nursery database. No real login, permissions, or data security.</div>', unsafe_allow_html=True)

children = st.session_state.children

def rows():
    return [{'Child ID':c['id'],'Child':c['name'],'Class':c['class'],'Status':c['status'],'Check-in':c['in'] or '—','Check-out':c['out'] or '—'} for c in children]

def pick_child(label='Select child'):
    ids = [c['id'] for c in children]
    selected = st.selectbox(label, ids, format_func=lambda i: next(c['name']+' · '+i for c in children if c['id']==i))
    return next(c for c in children if c['id']==selected)

if page == 'Login':
    st.subheader('Welcome to SmartNest')
    st.write('This is a role-selection demonstration. No password is checked or stored.')
    with st.form('demo_login'):
        username = st.text_input('Demo username', value='nursery.demo')
        st.text_input('Password (not validated)', type='password')
        submit = st.form_submit_button('Enter demo', type='primary')
    if submit:
        st.session_state.page = {'Staff':'Staff Dashboard','Parent':'Parent View','Administrator':'Staff Dashboard','Prospective parent':'Pre-enrollment'}[role]
        st.rerun()
    st.info('For a real system, authentication and permissions must be implemented on a secure server.')

elif page == 'Staff Dashboard':
    st.subheader('Today’s nursery overview')
    a,b,c = st.columns(3)
    a.metric('Enrolled children (sample)', len(children))
    b.metric('Present', sum(x['status']=='Present' for x in children))
    c.metric('Absent', sum(x['status']=='Absent' for x in children))
    st.subheader('Today’s attendance')
    st.dataframe(rows(), use_container_width=True, hide_index=True)
    st.subheader('Staff notes')
    st.write('• Check attendance at arrival and departure.\n\n• Confirm authorized pickup using the nursery’s existing identity checks.\n\n• Keep medical information restricted to approved staff.')

elif page == 'Attendance':
    st.write('Record a child’s arrival or departure. Changes last only during this browser session.')
    child = pick_child()
    st.write(f"**Current status:** {child['status']} · Check-in: {child['in'] or 'Not recorded'} · Check-out: {child['out'] or 'Not recorded'}")
    left,right = st.columns(2)
    if left.button('Check in', type='primary', disabled=child['status']=='Present'):
        child.update(status='Present', **{'in':datetime.now().strftime('%H:%M'),'out':''})
        st.success('Demo check-in recorded.'); st.rerun()
    if right.button('Check out', disabled=child['status']!='Present'):
        child.update(status='Checked out', **{'out':datetime.now().strftime('%H:%M')})
        st.success('Demo check-out recorded.'); st.rerun()
    st.dataframe(rows(), use_container_width=True, hide_index=True)

elif page == 'Child Profile':
    st.write('Example child information. Real medical records must be restricted by role.')
    child = pick_child()
    with st.form('profile'):
        name = st.text_input('Child name', child['name'])
        room = st.selectbox('Class', ['Blue Room','Yellow Room'], index=['Blue Room','Yellow Room'].index(child['class']))
        contact = st.text_input('Emergency contact (fictional)', child['contact'])
        allergy = st.text_input('Allergy note (fictional)', child['allergy'])

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

st.markdown('''<style>
.stApp {background:#f7f8fb;color:#243047} [data-testid="stSidebar"] {background:#fff;border-right:1px solid #e2e7ef}
h1,h2,h3 {color:#202d91;letter-spacing:-.02em} div.stButton>button[kind="primary"] {background:#202d91;border-color:#202d91}
[data-testid="stMetric"] {background:#fff;border:1px solid #e4e8ef;border-radius:8px;padding:16px}
[data-testid="stForm"] {background:white;border:1px solid #e4e8ef;border-radius:8px;padding:18px}
.small-note {color:#687487;font-size:.9rem} .prototype-note {padding:10px 14px;background:#fff4df;border-left:4px solid #f0bf50;border-radius:4px;margin:10px 0 18px}
</style>''', unsafe_allow_html=True)

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
        save = st.form_submit_button('Save demo changes', type='primary')
    if save:
        child.update(name=name, **{'class':room,'contact':contact,'allergy':allergy})
        st.success('Sample profile updated for this session.')

elif page == 'Parent View':
    st.subheader('My child')
    st.caption('Demo parent is linked only to fictional child SN-001. This is a visual simulation, not real access control.')
    child = children[0]
    a,b = st.columns(2)
    a.metric('Child', child['name']); b.metric('Attendance today', child['status'])
    st.write(f"**Class:** {child['class']}  |  **Check-in:** {child['in'] or '—'}  |  **Check-out:** {child['out'] or '—'}")
    st.subheader('Daily updates')
    for update in st.session_state.updates: st.info(update)

elif page == 'Consent':
    st.write('Authorized staff record whether parental consent was received. The prototype does not collect real signatures.')
    child = pick_child()
    with st.form('consent'):
        choice = st.selectbox('Consent status', ['Pending','Received','Declined'], index=['Pending','Received','Declined'].index(st.session_state.consents.get(child['id'],'Pending')))
        note = st.text_area('Administrative note (do not enter real personal data)')
        save = st.form_submit_button('Save consent status', type='primary')
    if save:
        st.session_state.consents[child['id']] = choice
        st.success('Demo consent status saved.')
    st.write('Recorded statuses:', st.session_state.consents or 'None yet')

elif page == 'Messages':
    st.write('Simple parent–staff messaging demonstration.')
    st.dataframe(st.session_state.messages, hide_index=True, use_container_width=True)
    with st.form('message'):
        to = st.selectbox('Send to', ['Nursery staff','Parent','Administrator'])
        message = st.text_area('Message', max_chars=300)
        send = st.form_submit_button('Send demo message', type='primary')
    if send:
        if message.strip():
            st.session_state.messages.append({'From':role,'To':to,'Message':message.strip()})
            st.success('Demo message added.'); st.rerun()
        else: st.warning('Write a message first.')

elif page == 'Search':
    query = st.text_input('Search by child name or ID')
    result = [r for r in rows() if query.lower() in (r['Child']+' '+r['Child ID']).lower()]
    st.dataframe(result, hide_index=True, use_container_width=True)
    st.caption('Search results show basic fields only. Sensitive records need permission checks in the real system.')

elif page == 'Reports':
    st.subheader('Attendance summary')
    st.dataframe(rows(), hide_index=True, use_container_width=True)
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows()[0]))
    writer.writeheader(); writer.writerows(rows())
    st.download_button('Download sample attendance CSV', data=buffer.getvalue(), file_name='smartnest_sample_attendance.csv', mime='text/csv')
    st.caption('This is a demo export, not an official SPEA report.')

elif page == 'Notifications':
    for notice in st.session_state.notices: st.info(notice)
    if role in ('Staff','Administrator'):
        with st.form('notice'):
            notice = st.text_input('New sample announcement')
            submit = st.form_submit_button('Add notification', type='primary')
        if submit and notice.strip():
            st.session_state.notices.insert(0, notice.strip()); st.rerun()

elif page == 'Pre-enrollment':
    st.write('Information only — full online applications are outside the current SmartNest scope.')
    for i,(heading,detail) in enumerate([
        ('Contact the nursery','Ask about availability, age groups, and opening hours.'),
        ('Review requirements','Request the nursery’s current documents and eligibility checklist.'),
        ('Arrange a visit','Speak with nursery administration about the enrollment process.'),
        ('Complete registration with the nursery','Submit documents through the nursery’s approved process, not this prototype.')],1):
        st.markdown(f'**Step {i}: {heading}**')
        st.write(detail)
    st.caption('No application form, payment, or document upload is included.')

st.divider()
st.caption('HCT SmartNest · Capstone Section 4.2 · UI/UX demonstration only · Fictional data')

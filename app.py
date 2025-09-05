import streamlit as st
import datetime
from main import fetch_questions, submit_quiz_results, fetch_quiz_results

st.set_page_config(layout="wide", page_title="Fizyoterapi Sınavı")

# Session state initialization
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'quiz_results' not in st.session_state:
    st.session_state.quiz_results = None
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'show_results_page' not in st.session_state:
    st.session_state.show_results_page = False
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = {}

st.title("Fizyoterapistler İçin Gelişim Sınavı")
st.markdown("Bilgilerinizi test edin ve eksiklerinizi görün.")

# --- UI for taking the quiz ---
if not st.session_state.show_results_page:
    with st.container():
        st.subheader("Sınava Başla")
        st.markdown("Lütfen isminizi girerek sınava başlayın.")
        st.session_state.username = st.text_input("Adınız ve Soyadınız", value=st.session_state.username)

        if st.button("Sınavı Başlat"):
            if st.session_state.username:
                st.session_state.questions = fetch_questions(exam_name="fizyoterapi_sinavi")
                st.session_state.quiz_started = True
            else:
                st.warning("Lütfen isminizi girin.")
    
    if st.session_state.quiz_started and st.session_state.questions:
        st.markdown("---")
        st.subheader("Sınav Soruları")
        
        with st.form("quiz_form"):
            user_answers = {}
            for i, q in enumerate(st.session_state.questions):
                st.markdown(f"**Soru {i+1}:** {q['question']}")
                answer_options = {option['text']: option['isCorrect'] for option in q['answerOptions']}
                selected_answer = st.radio(f"Cevabınızı seçin:", options=list(answer_options.keys()), key=f"q_{i}")
                user_answers[i] = selected_answer
                st.markdown("---")
            
            submit_button = st.form_submit_button("Sınavı Bitir ve Sonuçları Gönder")
            
            if submit_button:
                st.session_state.answers = user_answers
                
                # Calculate score
                score = 0
                correct_answers = {}
                for i, q in enumerate(st.session_state.questions):
                    correct_option = next(opt['text'] for opt in q['answerOptions'] if opt['isCorrect'])
                    correct_answers[i] = correct_option
                    if user_answers[i] == correct_option:
                        score += 1
                
                # Prepare data to submit
                quiz_data = {
                    "username": st.session_state.username,
                    "date": datetime.datetime.now().isoformat(),
                    "score": score,
                    "total_questions": len(st.session_state.questions),
                    "answers": user_answers,
                    "correct_answers": correct_answers
                }
                
                # Submit results to database
                submit_quiz_results(quiz_data)
                
                st.success(f"Tebrikler, {st.session_state.username}! Sınavı tamamladınız. Skorunuz: **{score}/{len(st.session_state.questions)}**")
                st.session_state.quiz_started = False
                st.session_state.quiz_results = quiz_data

# --- Admin view for showing all results ---
st.markdown("---")
st.subheader("Sınav Sonuçlarını Görüntüle (Yalnızca İlhami Hoca)")
password = st.text_input("Şifrenizi Girin", type="password")

if password == "12345": # Basit bir admin şifresi, gerçek uygulamada daha güvenli olmalı
    if st.button("Sonuçları Getir"):
        st.session_state.show_results_page = True
        with st.spinner("Sonuçlar yükleniyor..."):
            all_results = fetch_quiz_results()
            if all_results:
                st.success("Tüm sonuçlar başarıyla yüklendi.")
                # Display results in a table
                table_data = []
                for result in all_results:
                    table_data.append({
                        "Ad Soyad": result['username'],
                        "Tarih": result['date'].split('T')[0],
                        "Puan": f"{result['score']} / {result['total_questions']}"
                    })
                
                st.table(table_data)
            else:
                st.info("Henüz sınav sonucu bulunmamaktadır.")
else:
    st.warning("Yanlış şifre!")

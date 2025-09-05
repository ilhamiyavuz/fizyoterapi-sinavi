import datetime
from typing import List, Dict, Any
from google.cloud import firestore

# Pre-configured database client
# 'database=__app_id__' kısmını kaldırarak Firestore'un
# ortam değişkenlerinden proje kimliğini otomatik almasını sağlıyoruz.
db = firestore.Client()
collection_ref = db.collection("quiz_results")

def fetch_questions(exam_name: str) -> List[Dict[str, Any]]:
    """
    Simulates fetching quiz questions from a database.
    In a real app, this would query a dedicated 'questions' collection.
    """
    questions = [
        {
            "question": "Omuz ekleminin en sık karşılaşılan subluksasyon yönü hangisidir?",
            "answerOptions": [
                {"text": "Posterior", "isCorrect": False},
                {"text": "Anterior-inferior", "isCorrect": True},
                {"text": "Superior", "isCorrect": False},
                {"text": "Medial", "isCorrect": False}
            ]
        },
        {
            "question": "Parkinson hastalarında sıklıkla görülen 'donmuş yürüme' (freezing of gait) paternini azaltmak için hangi fizyoterapi tekniği en etkilidir?",
            "answerOptions": [
                {"text": "Yavaş, ritimsiz yürüme egzersizleri", "isCorrect": False},
                {"text": "Yüksek dirençli güçlendirme egzersizleri", "isCorrect": False},
                {"text": "Auditory (işitsel) veya görsel ipuçları kullanarak yürüme (Örn: metronom, yerdeki çizgiler)", "isCorrect": True},
                {"text": "Pasif eklem hareket açıklığı egzersizleri", "isCorrect": False}
            ]
        },
        {
            "question": "Serebral palsi (CP) olan bir çocukta spastisiteyi azaltmak için kullanılan bir fizyoterapi tekniği nedir?",
            "answerOptions": [
                {"text": "Ağırlık kaldırma egzersizleri", "isCorrect": False},
                {"text": "Dinamik germe ve güçlendirme egzersizleri", "isCorrect": False},
                {"text": "Proprioseptif Nöromusküler Fasilitasyon (PNF) teknikleri", "isCorrect": True},
                {"text": "Eklem içi kortizon enjeksiyonları", "isCorrect": False}
            ]
        },
        {
            "question": "Fibromiyalji sendromunda uygulanan aerobik egzersizlerin temel faydası aşağıdakilerden hangisidir?",
            "answerOptions": [
                {"text": "Sadece kas gücünü artırmak", "isCorrect": False},
                {"text": "Otonom sinir sistemini regüle etmek, uyku kalitesini ve ağrı eşiğini yükseltmek", "isCorrect": True},
                {"text": "Sadece eklem hareket açıklığını artırmak", "isCorrect": False},
                {"text": "Kemik mineral yoğunluğunu artırmak", "isCorrect": False}
            ]
        },
        {
            "question": "Pnömoni (zatürre) sonrası solunum fizyoterapisinde amaçlanan temel hedeflerden biri nedir?",
            "answerOptions": [
                {"text": "Kas gücünü artırmak için yüksek dirençli egzersizler uygulamak", "isCorrect": False},
                {"text": "Postural drenaj ve perküsyon teknikleriyle sekresyonları mobilize etmek", "isCorrect": True},
                {"text": "Sadece diyafragmatik solunum egzersizleri yaptırmak", "isCorrect": False},
                {"text": "Eklemlerdeki hareket kısıtlılığını gidermek", "isCorrect": False}
            ]
        },
    ]
    return questions

def submit_quiz_results(data: Dict[str, Any]):
    """
    Sınav sonuçlarını Firebase Firestore veritabanına kaydeder.
    """
    try:
        doc_ref = collection_ref.document()
        doc_ref.set(data)
        return True
    except Exception as e:
        print(f"Hata: Sonuçlar kaydedilemedi: {e}")
        return False

def fetch_quiz_results() -> List[Dict[str, Any]]:
    """
    Veritabanındaki tüm sınav sonuçlarını çeker.
    """
    try:
        docs = collection_ref.stream()
        results = [doc.to_dict() for doc in docs]
        return results
    except Exception as e:
        print(f"Hata: Sonuçlar çekilemedi: {e}")
        return []

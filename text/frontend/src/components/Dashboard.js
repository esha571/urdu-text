import React, { useState } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [inputText, setInputText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [languagePair, setLanguagePair] = useState('en-ur');

  const handleTranslate = async () => {
    const [sourceLang, targetLang] = languagePair.split('-');
    try {
        const response = await fetch('http://localhost:8000/translate/', {  // Make sure the URL is correct
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: inputText,
                source_lang: sourceLang,
                target_lang: targetLang,
            }),
        });

        if (!response.ok) {
            console.error('Server responded with:', response.status, response.statusText);
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        setTranslatedText(data.translated_text);
    } catch (error) {
        console.error('Error translating text:', error);
        setTranslatedText('Translation failed. Please try again.');
    }
};

  return (
    <div className="dashboard">
      <h1>Text Translator</h1>
      <div>
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter text here..."
          rows="10"
          cols="150"
        />
      </div>
      <div>
        <button onClick={handleTranslate}>Translate</button>
      </div>
      <div>
        <textarea
          value={translatedText}
          readOnly
          placeholder="Translated text will appear here..."
          rows="10"
          cols="150"
        />
      </div>
      <div>
        <label>
          Translate from:
          <select
            value={languagePair}
            onChange={(e) => setLanguagePair(e.target.value)}
          >
            <option value="en-ur">English to Urdu</option>
            <option value="ur-en">Urdu to English</option>
          </select>
        </label>
      </div>
    </div>
  );
};

export default Dashboard;

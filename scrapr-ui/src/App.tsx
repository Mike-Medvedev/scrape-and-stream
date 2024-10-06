import { TextInput } from '@mantine/core';
import styles from './App.module.css';
import { useEffect, useRef, useState } from 'react';
import openai from './assets/mantine-logo.svg';
import Markdown from 'markdown-to-jsx';

interface SyntaxHighlightedCodeProps {
  className?: string;
  children: React.ReactNode;
}
declare global {
  interface Window {
    hljs: any;
  }
}
function SyntaxHighlightedCode(props: SyntaxHighlightedCodeProps) {
  const ref = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (ref.current && props.className?.includes('lang-') && window.hljs) {
      window.hljs.highlightElement(ref.current);
      ref.current.removeAttribute('data-highlighted');
    }
  }, [props.className, props.children]);

  return (
    <div style={{ position: 'relative' }}>
      <CopyToClipboard text={props.children as string} />
      <code {...props} ref={ref} />
    </div>
  );
}

interface CopyToClipboardProps {
  text: string;
}

const CopyToClipboard = ({ text }: CopyToClipboardProps) => {
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  };

  return <button onClick={copyToClipboard}>Copy</button>;
};

type Role = 'assistant' | 'user' | 'system';
interface ChatMessage {
  role: Role;
  content: string;
}

const systemMessage: ChatMessage = {
  role: 'system',
  content: 'You are an assistant that answers questions based on the provided context.',
};

const App = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([systemMessage]);
  const [enterMessage, setEnterMessage] = useState<string>('');

  const handleEnterKey = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (enterMessage.trim()) {
        await submitMessage();
      }
    }
  };

  const handleClick = async () => {
    if (enterMessage.trim()) {
      await submitMessage();
    }
  };

  const submitMessage = async () => {
    const newMessage: ChatMessage = { role: 'user', content: enterMessage };

    setMessages(prev => [...prev, newMessage]);
    const updatedMessages = [...messages, newMessage];
    try {
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        body: JSON.stringify(updatedMessages),
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) throw Error('ERROR FETCHING');
      const result = await response.json();
      setMessages(result.messages);
    } catch (error) {
      console.log('ERROR IN FETCH', error);
    }

    setEnterMessage(''); // Clear input after submission
  };

  const conversation = messages.map((msg, index) => (
    <div className={styles.message} key={index}>
      {msg.role === 'user' ? (
        <div className={styles.user_message}>{msg.content}</div>
      ) : (
        <div style={{ display: 'flex', gap: '0.5rem', position: 'relative' }}>
          <div style={{ position: 'absolute', top: '-5px', left: '-40px' }}>
            <img src={openai} alt="openai_logo" width={30} height={30} />
          </div>
          <div className={styles.assistant_message}>
            {/* Render Markdown for assistant messages */}
            <Markdown
              children={msg.content}
              options={{
                overrides: {
                  code: SyntaxHighlightedCode,
                },
              }}
            />
          </div>
        </div>
      )}
    </div>
  ));

  return (
    <div className={styles.container}>
      <div className={styles.header}>Mantine UI expert</div>
      <div className={styles.chat_window}>
        <div className={styles.messages}>{conversation}</div>
      </div>
      <div className={styles.send_message}>
        <TextInput
          size="lg"
          value={enterMessage}
          onChange={e => setEnterMessage(e.target.value)}
          placeholder="Message Mantine Expert"
          onKeyDown={handleEnterKey}
          rightSection={
            <span
              className="material-symbols-outlined md-36"
              style={{ cursor: 'pointer' }}
              onClick={handleClick}>
              arrow_circle_up
            </span>
          }
        />
      </div>
      <div style={{ fontSize: '12px', textAlign: 'center' }}>
        ChatGPT can make mistakes. Check important info.
      </div>
    </div>
  );
};

export default App;

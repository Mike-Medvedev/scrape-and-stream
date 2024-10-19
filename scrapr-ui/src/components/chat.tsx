import { TextInput } from '@mantine/core';
import styles from './chat.module.css';
import { useState, useRef } from 'react';
import openai from '../assets/mantine-logo.svg';
import Markdown, { RuleType } from 'markdown-to-jsx';
import CodeBlock from './CodeBlock';
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
  const chatRef = useRef(null);

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
    const updatedMessages = [...messages, newMessage];
    setEnterMessage('');

    setTimeout(() => {
      if (chatRef.current) {
        (chatRef.current as HTMLDivElement).scrollTop = (chatRef.current as HTMLDivElement).scrollHeight;
      }
    }, 0);
    
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
          <Markdown
            options={{
              wrapper: 'article',
              overrides: {
                code: CodeBlock,
              },
              renderRule: (next, node, renderChildren) => {
                if (node.type === RuleType.codeInline) {
                  const modifiedNode = { ...node, type: RuleType.text };
                  return renderChildren([modifiedNode]);
                }
                return next();
              },
            }}
          >
            {msg.content}
          </Markdown>
          </div>
        </div>
      )}
    </div>
  ));

  return (
    <div className={styles.container}>
      <div className={styles.header}>Mantine UI expert</div>
      <div className={styles.chat_window} ref={chatRef}>
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

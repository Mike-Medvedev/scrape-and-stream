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
  
    return (
      <button 
        style={{
          backgroundColor: '#2C3E50', 
          color: '#FFFFFF', 
          border: 'none', 
          padding: '0.5rem', 
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '0.25rem'
        }} 
        onClick={copyToClipboard}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
        Copy
      </button>
    );
  };
export default CopyToClipboard;
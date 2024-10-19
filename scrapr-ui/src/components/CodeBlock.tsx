import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { a11yDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import CopyToClipboard from './CopyToClipboard';

const CodeBlock = ({ className, children }: { className?: string; children: string }) => {
    const language = className ? className.replace(/language-/, '').replace(/lang-/, '') : 'typescript';
    return (
      <div style={{display: 'flex', flexDirection: 'column', borderRadius: '0.5rem'}}>
        <div style={{ display: 'flex', width: '100%', justifyContent: 'space-between', backgroundColor: '#2C3E50', color: '#FFFFFF', padding: '0.5rem', borderTopLeftRadius: '0.5rem', borderTopRightRadius: '0.5rem'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: '0.25rem'}}>{language}</div>
          <CopyToClipboard text={children} />
        </div>
        <SyntaxHighlighter language={language} style={a11yDark} customStyle={{marginTop: '0px'}}>
          {children}
        </SyntaxHighlighter>
      </div>
    );
  };
  export default CodeBlock;
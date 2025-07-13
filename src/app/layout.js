import './globals.css';

export const metadata = {
  title: 'Test Series App',
  description: 'A test series platform built with Next.js and Django',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

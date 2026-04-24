import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';

export const metadata: Metadata = {
  title: 'Clinical Ops MVP',
  description: 'MVP interno para carga y revisión de documentos clínicos.',
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="es">
      <body>
        <header className="topbar">
          <nav className="container nav">
            <Link href="/">Inicio</Link>
            <Link href="/documents/new">Nuevo documento</Link>
          </nav>
        </header>
        <main className="container">{children}</main>
      </body>
    </html>
  );
}

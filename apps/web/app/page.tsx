import Link from 'next/link';

export default function HomePage() {
  return (
    <section>
      <h1>Clinical Ops — MVP interno</h1>
      <p>
        Flujo mínimo para cargar texto clínico, enviarlo a clinical-core y revisar
        el resultado inicial.
      </p>
      <ul>
        <li>
          <Link href="/documents/new">Crear y analizar documento clínico</Link>
        </li>
      </ul>
    </section>
  );
}

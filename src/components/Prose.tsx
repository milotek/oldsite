/**
 * Renders HTML produced by scripts/build-vault.ts.
 *
 * dangerouslySetInnerHTML is appropriate here and nowhere else: this string is
 * generated at build time from the vault by our own unified pipeline, never
 * from user input at runtime.
 */
export function Prose({ html }: { html: string }) {
  return <div className="prose" dangerouslySetInnerHTML={{ __html: html }} />
}

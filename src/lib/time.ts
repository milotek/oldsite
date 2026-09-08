export function isoDate(d: Date): string {
  return d.toISOString().slice(0, 10);
}

export function longDate(d: Date): string {
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
}

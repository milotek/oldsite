// BASE_URL always ends in a slash because trailingSlash is "always".
const base = import.meta.env.BASE_URL;

export function url(path = ''): string {
  return base + path.replace(/^\/+/, '');
}

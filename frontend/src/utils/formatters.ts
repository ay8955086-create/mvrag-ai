/**
 * Format duration in seconds into MM:SS or HH:MM:SS
 */
export function formatDuration(seconds: number): string {
  if (!seconds || isNaN(seconds)) return '00:00';
  const hrs = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);

  if (hrs > 0) {
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Format megabytes or bytes into readable string
 */
export function formatFileSize(sizeMb: number): string {
  if (!sizeMb || isNaN(sizeMb)) return '0 MB';
  if (sizeMb >= 1024) {
    return `${(sizeMb / 1024).toFixed(2)} GB`;
  }
  return `${sizeMb.toFixed(1)} MB`;
}

/**
 * Format ISO date string into human friendly date
 */
export function formatDate(isoString: string): string {
  if (!isoString) return 'N/A';
  try {
    const date = new Date(isoString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch (e) {
    return isoString;
  }
}

/**
 * Helper to get status color classes
 */
export function getStatusBadgeClass(status: string): string {
  switch (status) {
    case 'Completed':
      return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
    case 'Processing':
      return 'bg-amber-500/10 text-amber-400 border-amber-500/20 animate-pulse';
    case 'Pending':
      return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
    case 'Failed':
      return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
    default:
      return 'bg-slate-500/10 text-slate-400 border-slate-500/20';
  }
}

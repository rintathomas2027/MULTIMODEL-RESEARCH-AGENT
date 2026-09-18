/**
 * ScholarPulse / AI Study Assistant
 * React ES Module JavaScript Validation Engine
 */

export const PATTERNS = {
  EMAIL: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
  USERNAME: /^[a-zA-Z0-9_.-]{3,30}$/,
  URL: /^(https?:\/\/)([\da-z.-]+)\.([a-z.]{2,6})([/\w .~:?#[\]@!$&'()*+,;=-]*)*\/?$/i,
  ARXIV: /^(arxiv:)?(\d{4}\.\d{4,5}(v\d+)?|[a-z-]+(\.[A-Z]{2})?\/\d{7})$/i,
  DOI: /^10\.\d{4,9}\/[-._;()/:A-Za-z0-9]+$/i,
};

export const DOC_EXTENSIONS = ['pdf', 'txt', 'docx', 'doc', 'pptx', 'ppt', 'md', 'png', 'jpg', 'jpeg', 'webp'];
export const AUDIO_EXTENSIONS = ['mp3', 'wav', 'm4a', 'webm', 'ogg', 'aac', 'flac'];
export const MAX_DOC_SIZE_BYTES = 50 * 1024 * 1024; // 50MB for React modal
export const MAX_AUDIO_SIZE_BYTES = 25 * 1024 * 1024; // 25MB

export function validateRequired(value, fieldName = 'This field') {
  if (value === null || value === undefined) {
    return { isValid: false, message: `${fieldName} is required.` };
  }
  if (typeof value === 'string' && value.trim() === '') {
    return { isValid: false, message: `${fieldName} cannot be blank.` };
  }
  return { isValid: true, message: '' };
}

export function validateUsername(username) {
  if (!username || !username.trim()) {
    return { isValid: false, message: 'Username is required.' };
  }
  const trimmed = username.trim();
  if (trimmed.length < 3) {
    return { isValid: false, message: 'Username must be at least 3 characters long.' };
  }
  if (trimmed.length > 30) {
    return { isValid: false, message: 'Username cannot exceed 30 characters.' };
  }
  if (!PATTERNS.USERNAME.test(trimmed)) {
    return { isValid: false, message: 'Only letters, numbers, underscores, dots, or hyphens allowed.' };
  }
  return { isValid: true, message: 'Valid username' };
}

export function validateEmail(email, isRequired = true) {
  if (!email || !email.trim()) {
    if (!isRequired) return { isValid: true, message: '' };
    return { isValid: false, message: 'Email address is required.' };
  }
  const trimmed = email.trim();
  if (!PATTERNS.EMAIL.test(trimmed)) {
    return { isValid: false, message: 'Please enter a valid email address (e.g. user@university.edu).' };
  }
  return { isValid: true, message: 'Valid email' };
}

export function validatePassword(password, minLength = 6) {
  if (!password) {
    return {
      isValid: false,
      message: 'Password is required.',
      score: 0,
      label: 'Empty',
      color: '#ef4444'
    };
  }

  let score = 0;
  const length = password.length;

  if (length >= minLength) score += 1;
  if (length >= 8) score += 1;
  if (length >= 12) score += 1;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score += 1;
  if (/\d/.test(password)) score += 1;
  if (/[^a-zA-Z0-9]/.test(password)) score += 1;

  let label = 'Weak';
  let color = '#ef4444'; // Red

  if (score >= 5) {
    label = 'Strong';
    color = '#10b981'; // Green
  } else if (score >= 3) {
    label = 'Medium';
    color = '#f59e0b'; // Amber
  }

  if (length < minLength) {
    return {
      isValid: false,
      message: `Password must be at least ${minLength} characters.`,
      score,
      label,
      color
    };
  }

  return {
    isValid: true,
    message: `Password strength: ${label}`,
    score,
    label,
    color
  };
}

export function validatePasswordMatch(password, confirmPassword) {
  if (!confirmPassword) {
    return { isValid: false, message: 'Please confirm your password.' };
  }
  if (password !== confirmPassword) {
    return { isValid: false, message: 'Passwords do not match.' };
  }
  return { isValid: true, message: 'Passwords match' };
}

export function validateFile(file, options = {}) {
  const allowedExtensions = options.allowedExtensions || DOC_EXTENSIONS;
  const maxSizeBytes = options.maxSizeBytes || MAX_DOC_SIZE_BYTES;
  const maxSizeMB = (maxSizeBytes / (1024 * 1024)).toFixed(0);

  if (!file) {
    if (options.required) {
      return { isValid: false, message: 'Please select a file to upload.' };
    }
    return { isValid: true, message: '' };
  }

  if (file.size === 0) {
    return { isValid: false, message: 'The selected file is empty.' };
  }

  if (file.size > maxSizeBytes) {
    const currentMB = (file.size / (1024 * 1024)).toFixed(2);
    return {
      isValid: false,
      message: `File is too large (${currentMB}MB). Maximum allowed size is ${maxSizeMB}MB.`
    };
  }

  const extMatch = file.name.match(/\.([^.]+)$/);
  const ext = extMatch ? extMatch[1].toLowerCase() : '';
  if (!allowedExtensions.includes(ext)) {
    return {
      isValid: false,
      message: `Invalid file type (.${ext}). Supported formats: ${allowedExtensions.map(e => '.' + e).join(', ')}`
    };
  }

  return { isValid: true, message: `File accepted (${(file.size / (1024 * 1024)).toFixed(2)}MB)` };
}

export function validateUrl(url, isRequired = false) {
  if (!url || !url.trim()) {
    if (!isRequired) return { isValid: true, message: '' };
    return { isValid: false, message: 'URL is required.' };
  }
  const trimmed = url.trim();
  if (!/^https?:\/\//i.test(trimmed)) {
    return { isValid: false, message: 'URL must start with http:// or https://' };
  }
  if (!PATTERNS.URL.test(trimmed)) {
    return { isValid: false, message: 'Please enter a valid web address or direct paper URL.' };
  }
  return { isValid: true, message: 'Valid URL.' };
}

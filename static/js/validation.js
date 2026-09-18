/**
 * ScholarPulse / AI Study Assistant
 * Comprehensive Client-Side JavaScript Validation Engine
 * 
 * Features:
 * - Email, Username, Password, and Match Validators
 * - File Size & Extension Inspector
 * - URL, DOI, and ArXiv Format Validators
 * - Password Strength Meter & Complexity Scoring
 * - Inline DOM Feedback, Error Badges, & Input Highlighting
 * - Glassmorphic Toast Notification System
 * - Form Submit Interceptors & Shake Animations
 */

(function(global) {
    'use strict';

    const Validator = {
        // ==========================================
        // REGEX PATTERNS
        // ==========================================
        PATTERNS: {
            EMAIL: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
            USERNAME: /^[a-zA-Z0-9_.-]{3,30}$/,
            URL: /^(https?:\/\/)([\da-z.-]+)\.([a-z.]{2,6})([/\w .~:?#[\]@!$&'()*+,;=-]*)*\/?$/i,
            ARXIV: /^(arxiv:)?(\d{4}\.\d{4,5}(v\d+)?|[a-z-]+(\.[A-Z]{2})?\/\d{7})$/i,
            DOI: /^10\.\d{4,9}\/[-._;()/:A-Za-z0-9]+$/i,
            SAFE_TEXT: /^[^<>]*$/
        },

        // ==========================================
        // FILE CONFIGURATION
        // ==========================================
        DOC_EXTENSIONS: ['pdf', 'txt', 'docx', 'doc', 'pptx', 'ppt', 'md', 'png', 'jpg', 'jpeg', 'webp'],
        AUDIO_EXTENSIONS: ['mp3', 'wav', 'm4a', 'webm', 'ogg', 'aac', 'flac'],
        MAX_DOC_SIZE_BYTES: 15 * 1024 * 1024, // 15MB
        MAX_AUDIO_SIZE_BYTES: 25 * 1024 * 1024, // 25MB

        // ==========================================
        // VALIDATION METHODS
        // ==========================================
        
        /**
         * Validates required field
         */
        validateRequired(value, fieldName = 'This field') {
            if (value === null || value === undefined) {
                return { isValid: false, message: `${fieldName} is required.` };
            }
            if (typeof value === 'string' && value.trim() === '') {
                return { isValid: false, message: `${fieldName} cannot be blank.` };
            }
            return { isValid: true, message: '' };
        },

        /**
         * Validates username
         */
        validateUsername(username) {
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
            if (!this.PATTERNS.USERNAME.test(trimmed)) {
                return { isValid: false, message: 'Username can only contain letters, numbers, underscores, dots, or hyphens.' };
            }
            return { isValid: true, message: 'Username looks great!' };
        },

        /**
         * Validates email address
         */
        validateEmail(email, isRequired = true) {
            if (!email || !email.trim()) {
                if (!isRequired) return { isValid: true, message: '' };
                return { isValid: false, message: 'Email address is required.' };
            }
            const trimmed = email.trim();
            if (!this.PATTERNS.EMAIL.test(trimmed)) {
                return { isValid: false, message: 'Please enter a valid email address (e.g. user@university.edu).' };
            }
            return { isValid: true, message: 'Valid email address.' };
        },

        /**
         * Validates password and computes strength score
         */
        validatePassword(password, minLength = 6) {
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
        },

        /**
         * Validates that password and confirmPassword match
         */
        validatePasswordMatch(password, confirmPassword) {
            if (!confirmPassword) {
                return { isValid: false, message: 'Please confirm your password.' };
            }
            if (password !== confirmPassword) {
                return { isValid: false, message: 'Passwords do not match.' };
            }
            return { isValid: true, message: 'Passwords match perfectly!' };
        },

        /**
         * Validates file upload against allowed extensions and max size
         */
        validateFile(file, options = {}) {
            const allowedExtensions = options.allowedExtensions || this.DOC_EXTENSIONS;
            const maxSizeBytes = options.maxSizeBytes || this.MAX_DOC_SIZE_BYTES;
            const maxSizeMB = (maxSizeBytes / (1024 * 1024)).toFixed(0);

            if (!file) {
                if (options.required) {
                    return { isValid: false, message: 'Please select a file to upload.' };
                }
                return { isValid: true, message: '' };
            }

            // Check file size
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

            // Check file extension
            const extMatch = file.name.match(/\.([^.]+)$/);
            const ext = extMatch ? extMatch[1].toLowerCase() : '';
            if (!allowedExtensions.includes(ext)) {
                return {
                    isValid: false,
                    message: `Invalid file type (.${ext}). Supported formats: ${allowedExtensions.map(e => '.' + e).join(', ')}`
                };
            }

            return { isValid: true, message: `File accepted (${(file.size / (1024 * 1024)).toFixed(2)}MB)` };
        },

        /**
         * Validates URL format
         */
        validateUrl(url, isRequired = false) {
            if (!url || !url.trim()) {
                if (!isRequired) return { isValid: true, message: '' };
                return { isValid: false, message: 'URL is required.' };
            }
            const trimmed = url.trim();
            if (!/^https?:\/\//i.test(trimmed)) {
                return { isValid: false, message: 'URL must start with http:// or https://' };
            }
            if (!this.PATTERNS.URL.test(trimmed)) {
                return { isValid: false, message: 'Please enter a valid web address or direct paper URL.' };
            }
            return { isValid: true, message: 'Valid URL.' };
        },

        /**
         * Validates ArXiv ID, DOI or URL for external paper resolution
         */
        validateExternalPaperQuery(query) {
            if (!query || !query.trim()) {
                return { isValid: false, message: 'Please enter an ArXiv ID, DOI, or Paper URL.' };
            }
            const trimmed = query.trim();
            if (this.PATTERNS.ARXIV.test(trimmed)) {
                return { isValid: true, message: 'Detected ArXiv paper identifier.', type: 'arxiv' };
            }
            if (this.PATTERNS.DOI.test(trimmed)) {
                return { isValid: true, message: 'Detected Digital Object Identifier (DOI).', type: 'doi' };
            }
            if (this.PATTERNS.URL.test(trimmed)) {
                return { isValid: true, message: 'Detected direct paper URL.', type: 'url' };
            }
            return {
                isValid: false,
                message: 'Unrecognized format. Enter an ArXiv ID (e.g. 2303.08774), DOI (e.g. 10.1145/...), or Web URL.'
            };
        },

        /**
         * Validates text note / snippet
         */
        validateNotesText(text, minLength = 10, maxLength = 100000) {
            if (!text || !text.trim()) {
                return { isValid: false, message: 'Notes content cannot be empty.' };
            }
            const trimmed = text.trim();
            if (trimmed.length < minLength) {
                return { isValid: false, message: `Notes must contain at least ${minLength} characters for AI indexing.` };
            }
            if (trimmed.length > maxLength) {
                return { isValid: false, message: `Notes exceed the maximum length of ${maxLength} characters.` };
            }
            return { isValid: true, message: '' };
        },

        // ==========================================
        // UI MANIPULATION & FEEDBACK HELPERS
        // ==========================================

        /**
         * Displays error feedback next to an input element
         */
        showFieldError(inputEl, message) {
            if (!inputEl) return;
            inputEl.classList.remove('is-valid');
            inputEl.classList.add('is-invalid');

            // Find or create error element
            let errorEl = inputEl.parentNode.querySelector('.validation-msg-error');
            if (!errorEl) {
                errorEl = document.createElement('div');
                errorEl.className = 'validation-msg-error';
                inputEl.parentNode.appendChild(errorEl);
            }
            errorEl.innerHTML = `<span class="validation-icon">⚠️</span> ${message}`;
            errorEl.style.display = 'flex';

            // Clear any success element
            const successEl = inputEl.parentNode.querySelector('.validation-msg-success');
            if (successEl) successEl.style.display = 'none';
        },

        /**
         * Clears all validation feedback from an input element
         */
        clearFieldError(inputEl) {
            if (!inputEl) return;
            inputEl.classList.remove('is-invalid', 'is-valid');
            const errorEl = inputEl.parentNode.querySelector('.validation-msg-error');
            if (errorEl) errorEl.style.display = 'none';
            const successEl = inputEl.parentNode.querySelector('.validation-msg-success');
            if (successEl) successEl.style.display = 'none';
        },

        /**
         * Displays success feedback next to an input element
         */
        showFieldSuccess(inputEl, message = '') {
            if (!inputEl) return;
            inputEl.classList.remove('is-invalid');
            inputEl.classList.add('is-valid');

            const errorEl = inputEl.parentNode.querySelector('.validation-msg-error');
            if (errorEl) errorEl.style.display = 'none';

            if (message) {
                let successEl = inputEl.parentNode.querySelector('.validation-msg-success');
                if (!successEl) {
                    successEl = document.createElement('div');
                    successEl.className = 'validation-msg-success';
                    inputEl.parentNode.appendChild(successEl);
                }
                successEl.innerHTML = `<span class="validation-icon">✓</span> ${message}`;
                successEl.style.display = 'flex';
            }
        },

        /**
         * Triggers a subtle shake animation on invalid form element
         */
        shakeElement(el) {
            if (!el) return;
            el.classList.remove('shake-invalid');
            void el.offsetWidth; // Trigger reflow
            el.classList.add('shake-invalid');
            setTimeout(() => el.classList.remove('shake-invalid'), 600);
        },

        /**
         * Attaches a real-time Password Strength Meter beneath a password input
         */
        createPasswordStrengthMeter(passwordInputEl, containerEl) {
            if (!passwordInputEl) return;

            const targetContainer = containerEl || passwordInputEl.parentNode;
            let meterWrapper = targetContainer.querySelector('.password-strength-container');

            if (!meterWrapper) {
                meterWrapper = document.createElement('div');
                meterWrapper.className = 'password-strength-container';
                meterWrapper.innerHTML = `
                    <div class="strength-bar-wrapper">
                        <div class="strength-bar-fill" style="width: 0%; background: #ef4444;"></div>
                    </div>
                    <div class="strength-text" style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #94a3b8; margin-top: 4px;">
                        <span>Password Strength</span>
                        <strong class="strength-label" style="color: #ef4444;">Too Weak</strong>
                    </div>
                `;
                passwordInputEl.parentNode.appendChild(meterWrapper);
            }

            const fillEl = meterWrapper.querySelector('.strength-bar-fill');
            const labelEl = meterWrapper.querySelector('.strength-label');

            const updateMeter = () => {
                const val = passwordInputEl.value;
                if (!val) {
                    meterWrapper.style.display = 'none';
                    return;
                }
                meterWrapper.style.display = 'block';
                const res = this.validatePassword(val);
                
                let percentage = Math.min(100, Math.max(15, (res.score / 6) * 100));
                fillEl.style.width = `${percentage}%`;
                fillEl.style.background = res.color;
                labelEl.innerText = res.label;
                labelEl.style.color = res.color;
            };

            passwordInputEl.addEventListener('input', updateMeter);
            updateMeter();
        },

        /**
         * Attaches a show/hide password toggle button to an input
         */
        attachPasswordToggle(passwordInputEl) {
            if (!passwordInputEl) return;
            const parent = passwordInputEl.parentNode;
            if (parent.querySelector('.password-toggle-btn')) return;

            // Make sure parent has relative positioning
            const originalPosition = window.getComputedStyle(parent).position;
            if (originalPosition === 'static') {
                parent.style.position = 'relative';
            }

            const toggleBtn = document.createElement('button');
            toggleBtn.type = 'button';
            toggleBtn.className = 'password-toggle-btn';
            toggleBtn.setAttribute('aria-label', 'Toggle password visibility');
            toggleBtn.innerHTML = '👁️';
            toggleBtn.title = 'Show/Hide Password';

            toggleBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (passwordInputEl.type === 'password') {
                    passwordInputEl.type = 'text';
                    toggleBtn.innerHTML = '🙈';
                    toggleBtn.classList.add('active');
                } else {
                    passwordInputEl.type = 'password';
                    toggleBtn.innerHTML = '👁️';
                    toggleBtn.classList.remove('active');
                }
            });

            parent.appendChild(toggleBtn);
        },

        /**
         * Modern Glassmorphic Toast Notification System
         */
        showToast(message, type = 'info', duration = 3500) {
            let container = document.getElementById('toast-container');
            if (!container) {
                container = document.createElement('div');
                container.id = 'toast-container';
                container.className = 'toast-container';
                document.body.appendChild(container);
            }

            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;

            let icon = 'ℹ️';
            if (type === 'success') icon = '✅';
            if (type === 'error') icon = '❌';
            if (type === 'warning') icon = '⚠️';

            toast.innerHTML = `
                <div class="toast-icon">${icon}</div>
                <div class="toast-body">${message}</div>
                <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
            `;

            container.appendChild(toast);

            // Animate in
            requestAnimationFrame(() => {
                toast.classList.add('toast-show');
            });

            // Auto-dismiss
            setTimeout(() => {
                toast.classList.remove('toast-show');
                setTimeout(() => {
                    if (toast.parentElement) toast.remove();
                }, 300);
            }, duration);
        }
    };

    // ==========================================
    // AUTO-INITIALIZE COMMONLY USED FORMS ON DOM LOAD
    // ==========================================
    document.addEventListener('DOMContentLoaded', () => {
        // 1. Initialize all password fields with toggles
        document.querySelectorAll('input[type="password"]').forEach(input => {
            Validator.attachPasswordToggle(input);
        });

        // 2. Initialize Registration Password Strength Meter if register form is found
        const regPasswordInput = document.querySelector('form[action*="register"] input[name*="password"], #reg-password');
        if (regPasswordInput) {
            Validator.createPasswordStrengthMeter(regPasswordInput);
        }

        // 3. Auto-hook Login Form Validation
        const loginForm = document.querySelector('form[action*="login"]');
        if (loginForm) {
            const userInput = loginForm.querySelector('input[name="username"]');
            const passInput = loginForm.querySelector('input[name="password"]');

            if (userInput) {
                userInput.addEventListener('blur', () => {
                    const res = Validator.validateUsername(userInput.value);
                    if (!res.isValid) {
                        Validator.showFieldError(userInput, res.message);
                    } else {
                        Validator.clearFieldError(userInput);
                    }
                });
                userInput.addEventListener('input', () => Validator.clearFieldError(userInput));
            }

            if (passInput) {
                passInput.addEventListener('input', () => Validator.clearFieldError(passInput));
            }

            loginForm.addEventListener('submit', (e) => {
                let hasError = false;

                if (userInput) {
                    const userRes = Validator.validateUsername(userInput.value);
                    if (!userRes.isValid) {
                        Validator.showFieldError(userInput, userRes.message);
                        hasError = true;
                    }
                }

                if (passInput) {
                    const passRes = Validator.validatePassword(passInput.value, 1);
                    if (!passRes.isValid) {
                        Validator.showFieldError(passInput, passRes.message);
                        hasError = true;
                    }
                }

                if (hasError) {
                    e.preventDefault();
                    Validator.shakeElement(loginForm);
                    Validator.showToast('Please correct the highlighted errors before submitting.', 'warning');
                }
            });
        }

        // 4. Auto-hook Registration Form Validation
        const registerForm = document.querySelector('form[action*="register"]');
        if (registerForm) {
            const userInput = registerForm.querySelector('input[name="username"]');
            const emailInput = registerForm.querySelector('input[name="email"]');
            const pass1Input = registerForm.querySelector('input[name="password"], input[name="password1"]');
            const pass2Input = registerForm.querySelector('input[name="confirm_password"], input[name="password2"]');

            if (userInput) {
                userInput.addEventListener('blur', () => {
                    const res = Validator.validateUsername(userInput.value);
                    if (!res.isValid) {
                        Validator.showFieldError(userInput, res.message);
                    } else {
                        Validator.showFieldSuccess(userInput, 'Valid username');
                    }
                });
                userInput.addEventListener('input', () => Validator.clearFieldError(userInput));
            }

            if (emailInput) {
                emailInput.addEventListener('blur', () => {
                    const res = Validator.validateEmail(emailInput.value);
                    if (!res.isValid) {
                        Validator.showFieldError(emailInput, res.message);
                    } else {
                        Validator.showFieldSuccess(emailInput, 'Valid email address');
                    }
                });
                emailInput.addEventListener('input', () => Validator.clearFieldError(emailInput));
            }

            if (pass1Input) {
                pass1Input.addEventListener('input', () => {
                    Validator.clearFieldError(pass1Input);
                    if (pass2Input && pass2Input.value) {
                        const matchRes = Validator.validatePasswordMatch(pass1Input.value, pass2Input.value);
                        if (!matchRes.isValid) {
                            Validator.showFieldError(pass2Input, matchRes.message);
                        } else {
                            Validator.showFieldSuccess(pass2Input, matchRes.message);
                        }
                    }
                });
            }

            if (pass2Input) {
                pass2Input.addEventListener('input', () => {
                    if (pass1Input) {
                        const matchRes = Validator.validatePasswordMatch(pass1Input.value, pass2Input.value);
                        if (!matchRes.isValid) {
                            Validator.showFieldError(pass2Input, matchRes.message);
                        } else {
                            Validator.showFieldSuccess(pass2Input, matchRes.message);
                        }
                    }
                });
            }

            registerForm.addEventListener('submit', (e) => {
                let hasError = false;

                if (userInput) {
                    const userRes = Validator.validateUsername(userInput.value);
                    if (!userRes.isValid) {
                        Validator.showFieldError(userInput, userRes.message);
                        hasError = true;
                    }
                }

                if (emailInput && emailInput.value) {
                    const emailRes = Validator.validateEmail(emailInput.value);
                    if (!emailRes.isValid) {
                        Validator.showFieldError(emailInput, emailRes.message);
                        hasError = true;
                    }
                }

                if (pass1Input) {
                    const passRes = Validator.validatePassword(pass1Input.value, 6);
                    if (!passRes.isValid) {
                        Validator.showFieldError(pass1Input, passRes.message);
                        hasError = true;
                    }
                }

                if (pass2Input && pass1Input) {
                    const matchRes = Validator.validatePasswordMatch(pass1Input.value, pass2Input.value);
                    if (!matchRes.isValid) {
                        Validator.showFieldError(pass2Input, matchRes.message);
                        hasError = true;
                    }
                }

                if (hasError) {
                    e.preventDefault();
                    Validator.shakeElement(registerForm);
                    Validator.showToast('Please fix the errors in the registration form.', 'error');
                }
            });
        }
    });

    // Expose globally
    global.ScholarValidator = Validator;

})(typeof window !== 'undefined' ? window : this);

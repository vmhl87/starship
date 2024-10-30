function decrypt(ciphertext, k) {
	const key = CryptoJS.enc.Utf8.parse(k.padEnd(16, '0'));
	const decrypted = CryptoJS.AES.decrypt(ciphertext, key, {mode:CryptoJS.mode.ECB});
	return decrypted.toString(CryptoJS.enc.Utf8);
}

function trypass(key) {
	let work = {val: 1};

	const decr_recursive = (element, key, work) => {
		if(element.nodeType === Node.ELEMENT_NODE) {
			element.childNodes.forEach(child => {
				decr_recursive(child, key, work);
				if(!work.val) return;
			});

			if(element.childNodes.length == 1) {
				try{
					const decrypted = decrypt(element.textContent, key);
					if(decrypted.length == 0) {
						work.val = 0;
					}else{
						element.textContent = decrypted;
					}
				}catch(e){}
			}
		}
	}

	const enchblocks = document.querySelectorAll('.protected-content');
	enchblocks.forEach(element => {
		decr_recursive(element, key, work);
	});

	if(work.val) {
		enchblocks.forEach(element => {
			element.classList.remove('protected-content');
			element.classList.add('unprotected-content');
		});

		const protnotice = document.querySelectorAll('.protection-notice');
		protnotice.forEach(element => { element.remove(); });
	}
};

function decrypt_challenge() {
	const overlay = document.createElement('div');
	overlay.style.position = 'fixed';
	overlay.style.top = '0';
	overlay.style.left = '0';
	overlay.style.width = '100%';
	overlay.style.height = '100%';
	overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
	overlay.style.zIndex = '999';

	document.body.appendChild(overlay);

	const floatingBox = document.createElement('div');
	floatingBox.style.position = 'fixed';
	floatingBox.style.top = '50%';
	floatingBox.style.left = '50%';
	floatingBox.style.transform = 'translate(-50%, -50%)';
	floatingBox.style.padding = '20px';
	floatingBox.style.backgroundColor = '#404040';
	floatingBox.style.zIndex = '1000';

	const passwordInput = document.createElement('input');
	passwordInput.type = 'password';
	passwordInput.placeholder = 'Enter passphrase';
	passwordInput.style.marginBottom = 'auto';
	passwordInput.style.marginTop = 'auto';
	passwordInput.style.width = 'auto';
	passwordInput.style.padding = '8px';
	passwordInput.style.border = 'none';
	passwordInput.style.outline = 'none';
	passwordInput.style.color = '#A0A0A0';
	passwordInput.style.backgroundColor = '#151515';
	floatingBox.appendChild(passwordInput);

	const submitPassword = () => {
		document.body.removeChild(floatingBox);
		document.body.removeChild(overlay);
		trypass(passwordInput.value);
	};

	const confirmButton = document.createElement('button');
	confirmButton.textContent = 'Decrypt';
	confirmButton.style.padding = '8px';
	confirmButton.style.border = 'none';
	confirmButton.style.backgroundColor = '#808080';
	confirmButton.style.color = 'white';
	confirmButton.style.cursor = 'pointer';
	confirmButton.addEventListener('click', submitPassword);
	floatingBox.appendChild(confirmButton);

	passwordInput.addEventListener('keypress', (event) => {
		if (event.key === 'Enter') {
			submitPassword();
		}
	});

	document.body.appendChild(floatingBox);
	passwordInput.focus();
}

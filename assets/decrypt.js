function raw_decrypt(ciphertext, k) {
	const key = CryptoJS.enc.Utf8.parse(k.padEnd(16, '0'));
	const decrypted = CryptoJS.AES.decrypt(ciphertext, key, {mode:CryptoJS.mode.ECB});
	return decrypted.toString(CryptoJS.enc.Utf8);
}

function splay(str, base, idx) {
	let res = "";

	for(let i=idx; i<str.length; i+=base) {
		res += str[i];
	}

	return res;
}

function weave(strings, base) {
	let res = "";

	for(let idx=0, pos=0; pos<strings[idx].length;) {
		res += strings[idx][pos];
		++idx;
		if(idx == base) {
			idx = 0;
			++pos;
		}
	}

	return res;
}

function decrypt(ciphertext, key) {
	let keys = 1 + Math.floor(key.length / 16),
		decrypted = [];

	for(let i=0; i<keys; ++i) {
		decrypted.push(raw_decrypt(splay(ciphertext, keys, i), splay(key, keys, i)));
	}

	return weave(decrypted, keys);
}

function trypass(key, root) {
	work = {val: true};

	const decr_recursive = (element, key, work) => {
		if(element.nodeType === Node.ELEMENT_NODE) {
			element.childNodes.forEach(child => {
				if(work.val) decr_recursive(child, key, work);
			});

			if(element.childNodes.length == 1 && element.childNodes[0].childNodes.length == 0) {
				try{
					const decrypted = decrypt(element.textContent, key);
					if(decrypted.length == 0) {
						work.val = false;
					}else{
						element.innerHTML = decrypted;
					}
				}catch(e){
					work.val = false;
				}
			}
		}
	}

	decr_recursive(root.childNodes[3], key, work);

	if(work.val) {
		root.childNodes[3].classList.remove('protected-content');
		root.childNodes[3].classList.add('unprotected-content');
		root.childNodes[1].remove();
	}
};

function decrypt_challenge(elem) {
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
	floatingBox.style.padding = '10px';
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
		trypass(passwordInput.value, elem.parentNode.parentNode);
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

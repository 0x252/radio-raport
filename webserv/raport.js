const delButton = document.getElementById('delQSO')
				const updateButton = document.getElementById('modifyQSO')
				const readButton = document.getElementById('readButton')
				const addButton = document.getElementById('addQSOButton')
	
				/* DEL BUTTON logic*/
				delButton.onclick = async () => {
					const qsoID = parseInt(document.getElementById('qsoDeleteID').value);
					if(qsoID < 0) {
						return alert("Плохой ID")
					}
					// XSS?
					const res = await fetch(`/api/QSOdel/${qsoID}`,
					{
						method: "DELETE"
					})
					if (res.ok) {
						res.json().then((js) => {
							console.log(js)
						})
					} else {
						alert("del qso err")
						console.log(res)
					}
					/* TODO: удалить запись */
				}
				/*update button logic*/
				updateButton.onclick = async() => {
					/* TODO: обновить запись */
						const qsoID = parseInt(document.getElementById('qsoUpdateID').value);
						if(qsoID < 0) {
							return alert("Плохой ID")
						}
						const data = {
							qsoUpdateID: qsoID,
					        callsignA: document.getElementById("callsignUpdateInputA").value,
					        callsignB: document.getElementById("callsignUpdateInputB").value,
					        RSTA: document.getElementById("RSTUpdateA").value,
					        RSTB: document.getElementById("RSTUpdateB").value,
					    };
					    const res = await fetch(`/api/QSOPut/${qsoID}`, {
					        method: 'PUT',  
					        headers: {
					            'Content-Type': 'application/json',  
					        },
					        body: JSON.stringify(data) 
					    });
					    if(!res.ok) {
					    	console.log(res)
					    	return alert("Ошибка в изменение")
					    }
					    res.json().then((js) => {
					    	console.log(js)
					    })
				}
				/* Add button logic */
				addButton.onclick = async () => {
					console.log("add record")
					    const data = {
					        callsignA: document.getElementById("callsignInputA_create").value,
					        callsignB: document.getElementById("callsignInputB_create").value,
					        RSTA: document.getElementById("RSTA_create").value,
					        RSTB: document.getElementById("RSTB_create").value,
					    };
					    try {
					    	const res = await fetch("/api/addQSO", {
					    		method: "POST",
					    		headers: {
					    			"Content-Type": "application/json"
					    		},
					    		body: JSON.stringify(data)
					    	})
					    	if (res.ok) {
					    		const resJson = res.json().then( (js) => {
					    			console.log(js)
					    			if(js.error) {
					    				alert(`Ошибка: ${js.error}`)
					    			} else {
					    				alert("QSO Добавлено")
					    			}
					    		})
					    	} else {
					    		console.log(res)
					    		alert("Ошибка при добавление QSO")
					    	}
					    }catch(error) {
					    	console.err(error)
					    }
				} /* end  add button logic */
				readButton.onclick = async () => {
					//XSS?
					limit = document.getElementById('qsoLimit').value
					offset = document.getElementById('qsoOffset').value
					const res = await fetch(`/api/QSO?limit=${limit}&offset=${offset}`, {
						method: "GET",
					})
					if (res.ok) {
						res.json().then( (js) => {
							console.log(`JS: ${js}`)
							console.log(js)
						})
					} else {
						console.log(`[errget]: ${res}`)
					}
				}
const btn = document.getElementById("btn")
const input = document.getElementById("input")
const file = document.getElementById("file")

const imgOutput = document.getElementById("imgOutput")
const fastPrisOutput = document.getElementById("fastPrisOutput")
const snittBrukOutput = document.getElementById("snittBrukOutput")
const spotPrisOutput = document.getElementById("spotPrisOutput")



btn.onclick = () => {

    let formData = new FormData();
    if (file.files[0] != null) {// if file exists
        formData.append("file", file.files[0])
        console.log(formData.get('file'))
    } else {
        formData.append("file", "0")
        console.log(formData.get('file'))
    }
    fetch("http://127.0.0.1:5000/sendFile", {
        method: "POST",
        body: formData,
    }).then(async response => {
        if (response.ok) {
            fetch("http://127.0.0.1:5000/createPlot", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "value": input.value, "radio": document.querySelector('input[name="spotArea"]:checked').value }),
            }).then(async response => {
                if (response.ok) {
                    response.text().then(async result => {
                        imgOutput.src = "data:image/png;base64, " + result
                        return
                    })
                    return

                }
                throw new Error('Request failed!');
            }, networkError => {
                console.log(networkError.message);
            })

            fetch("http://127.0.0.1:5000/fastPris", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "value": input.value }),
            }).then(async response => {
                if (response.ok) {
                    response.text().then(async result => {
                        console.log(result)
                        results = result.split("_")
                        fastPrisOutput.innerText = "Ditt total beløp over perioden er: " + results[0] + " kr for " + input.value + " kr/kWh"
                        snittBrukOutput.innerText = "Ditt gjennomsnittlig forbruk over perioden er: " + results[1] + " kWh"
                        spotPrisOutput.innerText = "Din spotpris total beløp over perioden er: " + results[2] + " kr"
                        return
                    })
                    return

                }
                throw new Error('Request failed!');
            }, networkError => {
                console.log(networkError.message);
            })
        }
    })


}
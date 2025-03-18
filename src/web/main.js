import { API_URL } from "./config.js";

async function fetchNumber() {
    try {
        const response = await fetch(API_URL+"/increment");
        const data = await response.json();
        document.getElementById("number").innerText = data.counter;
    } catch (error) {
        console.error("Error fetching number:", error);
        document.getElementById("number").innerText = "Error";
    }
}

document.addEventListener("DOMContentLoaded", fetchNumber);
document.getElementById("fetchButton").addEventListener("click", fetchNumber);

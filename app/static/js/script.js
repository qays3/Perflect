document.addEventListener("click", (event) => {
 
    const effect = document.createElement("div");
    effect.classList.add("click-effect");
  
 
    effect.style.left = `${event.pageX - 10}px`;
    effect.style.top = `${event.pageY - 10}px`;
  
 
    document.body.appendChild(effect);
 
    effect.addEventListener("animationend", () => {
      effect.remove();
    });
  });
  
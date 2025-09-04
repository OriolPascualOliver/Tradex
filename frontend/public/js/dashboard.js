(function(){
  function setState(widget, state){
    widget.dataset.state = state;
    if(state === 'loading'){
      const placeholder = widget.querySelector('[data-role="slow"]');
      if(placeholder){
        placeholder.textContent = 'Cargando datos…';
        widget._slowTimer = setTimeout(()=>{
          if(widget.dataset.state === 'loading'){
            placeholder.textContent = 'Tarda más de lo habitual…';
          }
        }, 10000);
      }
    } else if(widget._slowTimer){
      clearTimeout(widget._slowTimer);
    }
  }

  document.addEventListener('DOMContentLoaded', ()=>{
    document.querySelectorAll('[data-widget]').forEach(widget=>{
      widget.setAttribute('tabindex','-1');
      const retry = widget.querySelector('.retry');
      if(retry){
        retry.addEventListener('click', e=>{
          e.preventDefault();
          setState(widget, 'loading');
          setTimeout(()=>setState(widget, 'success'), 800);
          widget.focus();
        });
      }
    });
  });
})();

console.log('hijacking');
EventTarget.prototype.addEventListener = function(...args) {
  console.log(args);
}


function awaitEl (selector, timeout = 5000, interval = 150) {
  const startTime = Date.now();
  return new Promise(function lookForEl(resolve, reject) {
    const el = document.querySelector(selector);

    if (el) {
      return resolve(el);
    }

    if (Date.now() - startTime > timeout) {
      return reject('timeout')
    }

    setTimeout(() => lookForEl(resolve, reject), interval);
  });
}



function injectLooperUI (progressBar) {
  const looper = document.createElement('div');
  looper.classList = 'looper ';

  let draggingEl = null;
  const handles = ['left', 'right'].map(cls => {
    const handle = document.createElement('div');
    handle.classList = `lp-handle ${cls}`;
    looper.appendChild(handle);
    handle.addEventListener('mousedown', e => {
      draggingEl = handle;
      e.preventDefault();
      e.stopPropagation();
      document.addEventListener('mouseup', stopDrag, true);
      document.addEventListener('mousemove', onDrag, true);
      document.addEventListener('click', stopDrag, true);
    });
    return handle;
  });
  progressBar.appendChild(looper);

  function onDrag (e) {
    let sign = 1;
    if (draggingEl == handles[0]) {
      looper.style.left = (looper.offsetLeft + e.movementX) + 'px';
      sign = -1;
    }
    looper.style.width = (Math.max(40, looper.offsetWidth + (e.movementX * sign))) + 'px';
  }

  function stopDrag (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    document.removeEventListener('mouseup', stopDrag, true);
    document.removeEventListener('mousemove', onDrag, true);
    document.removeEventListener('click', stopDrag, true);
  }



}

awaitEl('.ytp-progress-bar-container').then(injectLooperUI);

// awaitEl('#player-theater-container').then(function (player) {
//   document.addEventListener('mouseup', e => {
//     e.stopImmediatePropagation();
//     e.preventDefault();
//   }, true);
//   document.addEventListener('click', e => {
//     e.stopImmediatePropagation();
//     e.preventDefault();
//   }, true);
//   document.addEventListener('mousedown', e => {
//     e.stopImmediatePropagation();
//     e.preventDefault();
//   }, true);
// });

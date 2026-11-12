// Freiwilliges WhatsApp-Teilen, ohne Telefonnummer, API oder automatische Nachrichten.
(() => {
  const whatsappLink = (message) => 'https://wa.me/?text=' + encodeURIComponent(message);
  const siteUrl = 'https://keschflow.github.io/Nichts_Institut/';

  function addShareLink(id, label, afterElement) {
    if (!afterElement || document.getElementById(id)) return null;
    const link = document.createElement('a');
    link.id = id;
    link.className = 'btn light';
    link.textContent = label;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    afterElement.insertAdjacentElement('afterend', link);
    return link;
  }

  const pageLink = addShareLink(
    'share-whatsapp',
    'Per WhatsApp weiterreichen ↗',
    document.getElementById('share')
  );
  if (pageLink) {
    pageLink.href = whatsappLink(
      'VEB Kombinat der LPG des Nichts – wir machen nichts. Aber richtig. ' +
      'Hier kannst du dir deinen amtlichen Nichtstun-Bescheid ausstellen lassen: ' + siteUrl
    );
  }

  const caseLink = addShareLink(
    'share-whatsapp-case',
    'Bescheid per WhatsApp ↗',
    document.getElementById('share-case')
  );
  if (!caseLink) return;
  caseLink.hidden = true;

  const issue = document.getElementById('issue');
  if (!issue) return;
  issue.addEventListener('click', () => {
    const number = document.getElementById('case-number').textContent;
    const heading = document.getElementById('case-heading').textContent;
    const topic = document.getElementById('case-topic').textContent;
    const body = document.getElementById('case-body').textContent;
    caseLink.href = whatsappLink([
      'VEB Kombinat der LPG des Nichts',
      'Mein amtlicher Nichtstun-Bescheid:',
      number,
      heading,
      topic,
      body,
      'Auch Nichtstun beantragen: ' + siteUrl
    ].join('\n'));
    caseLink.hidden = false;
  });
})();

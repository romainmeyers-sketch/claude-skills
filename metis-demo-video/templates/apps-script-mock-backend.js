/* Demo-only fake Apps Script backend. Runs before the hub's own code so BACKEND is true
   and no real data is ever read or written. People are real Metis names per the brief. */
(function(){
  var EMAIL = 'rohan.ray@metisstrategy.com';
  var DB = {state: null, rev: 'r1'};
  var DAYS = [['Tue, Oct 13', 13], ['Wed, Oct 14', 14], ['Thu, Oct 15', 15]];
  var TIMES = [['9:30 AM', 16, 30], ['10:30 AM', 17, 30], ['1:00 PM', 20, 0], ['2:30 PM', 21, 30], ['4:00 PM', 23, 0]];
  function slots(d){
    var out = [];
    TIMES.forEach(function(t, i){
      if ((d + i) % 4 === 0) return;                        // a few gaps so it looks like a real calendar
      var s = new Date(Date.UTC(2026, 9, d, t[1], t[2])), e = new Date(s.getTime() + 30 * 60000);
      out.push({label: t[0], start: s.toISOString(), end: e.toISOString()});
    });
    return out;
  }
  var api = {
    getBootstrap: function(){ return {ok: true, email: EMAIL, admin: false, tester: false, state: DB.state, rev: DB.rev}; },
    saveState: function(json, rev){ try{ DB.state = JSON.parse(json); }catch(e){} DB.rev = 'r' + (Date.now() % 100000); return {ok: true, rev: DB.rev}; },
    getAvailability: function(email, myTz, theirTz){
      return {ok: true, tz: 'America/Los_Angeles', tzLabel: 'PDT', sameZone: true, theirZone: 'PDT', mutual: true, daysOut: 1,
              days: DAYS.map(function(d){ return {day: d[0], slots: slots(d[1])}; })};
    },
    getDirectory: function(){ return {ok: true, profiles: {}}; },
    getSubscriptions: function(){ return {ok: true, items: []}; },
    reportSyncBlocked: function(){ return {ok: true}; },
    resetState: function(){ return {ok: true}; },
    sendMentorPrefs: function(){ return {ok: true}; },
    sendImei: function(){ return {ok: true}; },
    setAdminPrefs: function(){ return {ok: true}; },
    setAdminTodo: function(){ return {ok: true}; }
  };
  function chain(){
    var ok = function(){}, fail = function(){};
    var o = new Proxy({}, {get: function(_, name){
      if (name === 'withSuccessHandler') return function(f){ ok = f; return o; };
      if (name === 'withFailureHandler') return function(f){ fail = f; return o; };
      return function(){
        var args = [].slice.call(arguments), delay = name === 'getAvailability' ? 650 : 120;
        setTimeout(function(){
          try{ ok(api[name] ? api[name].apply(null, args) : {ok: true}); }catch(e){ fail(e); }
        }, delay);
      };
    }});
    return o;
  }
  window.google = {script: {run: new Proxy({}, {get: function(_, n){ return chain()[n]; }})}};
})();

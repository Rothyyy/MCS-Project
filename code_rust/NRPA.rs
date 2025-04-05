use std::collections::HashMap;
use crate::tools::resultSaver::writeLine;
use std::time::Instant;
use ndarray_rand::rand::SeedableRng;
use rand::Rng;
use rand_chacha::{ChaCha20Rng, ChaChaRng};
use crate::methods::NMCS_2::PLAYOUT;

// IMPORT STATE and MOVE:
use crate::models::conjectures::spectralgap::{Move, State};


pub struct NRPA{
    pub best_yet : f64,
    pub timeout : f64,
    pub registerName : String,
    pub start_time : Instant,
}

impl NRPA{
    pub fn new() -> Self {
        Self{ start_time : Instant::now(),best_yet: 0.0, timeout : -1.0, registerName : String::new() }
    }

    pub fn random_move(&self, moves : Vec<Move>, policy: &mut HashMap<Move, f64>, rng: &mut ChaCha20Rng) -> Move{

        let mut sum : f64 = 0.0;

        for &mv  in &moves {
            match policy.get(&mv){
                Some(v) => sum += v.exp(),
                None => {policy.insert(mv, 0.0); sum+=1.0}
            };

        }

        //let stop = sum*rand::random::<f64>();
        let stop = sum*rng.gen::<f64>();;
        sum = 0.0;
        for &mv in &moves {
            sum += policy.get(&mv).unwrap().exp();
            if sum > stop {
                return mv;
            }
        }
        return moves[0];
    }

    pub fn playout(&self, mut st : State, mut policy : HashMap<Move, f64>, rng: &mut ChaCha20Rng) -> State{
        /*
        while !st.terminal() {
            let  moves: Vec<Move> = st.legal_moves();
            if moves.len() == 0 {
                return st;
            }
            let mv = random_move(moves, &mut policy);
            st.play(mv);
        }
        //println!("playout : {}, {}, {}",st.score(), st.n_sommet, st.n_arete );
        return st;

         */

        let mut best_state: State = st.clone(); //State::new();
        let mut best_state_score = best_state.score();

        while !st.terminal() {
            let  moves: Vec<Move> = st.legal_moves(rng);
            if moves.len() == 0 {
                //return st;
                best_state.no_improvement_possible = true;
                return best_state;
            }
            let mv = self.random_move(moves, &mut policy, rng);
            st.play(mv);

            if State::CONSIDER_NON_TERM {
                let sc = st.score();
                if sc > best_state_score {
                    best_state_score = sc;
                    best_state = st.clone();
                    best_state.best_score = sc;
                }
            }
        }
        if State::CONSIDER_NON_TERM{
            return best_state;
        }
        //println!("playout : {}, {}, {}",st.score(), st.n_sommet, st.n_arete );
        return st;

    }

    pub fn adapt(&self, mut policy: HashMap<Move, f64>, st : &mut State, ini_state : State, rng: &mut ChaCha20Rng) -> HashMap<Move, f64>{
        //let mut s = State::new();

        let mut s: State = ini_state.clone();
        let mut polp: HashMap<Move, f64> = policy.clone();
        for best in &mut st.seq[..] {
            let moves = s.legal_moves(rng);
            let mut sum = 0.0;
            for &m in &moves {
                match policy.get(&m){
                    Some(v) => sum += v.exp(),
                    None => {policy.insert(m, 0.0); sum += 1.0}
                };
            }

            for &m in &moves {
                match polp.get(&m){
                    Some(v) => polp.insert(m, v - policy.get(&m).unwrap().exp()/sum),
                    None => polp.insert(m, -policy.get(&m).unwrap().exp()/sum)
                };

            }
            polp.insert(*best, polp.get(&best).unwrap() + 1.0);
            s.play(*best);
        }
        return polp;
    }

    pub fn nrpa(&mut self, level : i8, mut policy: HashMap<Move, f64>, ini_state : State, initial : bool, rng: &mut ChaCha20Rng) -> State {
        //let mut st: State = State::new();
        let mut st: State = ini_state.clone();
        let mut stscore : f64 = st.score();

        let mut best_state: State = st.clone(); //State::new();
        let mut best_state_score = best_state.score();

        if level == 0 || self.start_time.elapsed().as_secs_f64() > self.timeout {
            return self.playout(st, policy, rng);
        }

        //pour le test, à retirer
        //let mut n = 100;
        let mut n = PLAYOUT;

        for i in 0..n {
            if initial {println!("NRPA loop {}, best score : {} {}", i, stscore, best_state_score);
                //println!("{}", st.adj_mat);
            }
            let pol : HashMap<Move, f64> = policy.clone();
            let mut s = self.nrpa(level-1, pol, ini_state.clone(), false, rng);
            let s_score = s.score();


            if stscore < s_score {
                st = s.clone();
                stscore = s_score;

                //if stscore > self.best_yet {
                if stscore > best_state_score {
                    //self.best_yet = stscore;
                    best_state_score = stscore;
                    best_state.best_score = stscore;
                    best_state = st.clone();
                    println!("NRPA best score yet : {}", best_state.best_score);
                    /*let elapsed = self.start_time.elapsed().as_secs_f64();
                    writeLine(elapsed.to_string() + " " + &*stscore.to_string()+ "\n", self.registerName.clone());
                    if true {
                        println!("NRPA best score yet : {} after {}", stscore, elapsed);
                    }*/
                }

            }
            policy = self.adapt(policy, &mut st, ini_state.clone(), rng);
        }
        //return st;
        return best_state;
    }
}


pub fn launch_nrpa(level : i8, ini_state : State, timeout : f64, registerName : String) -> State {
    let mut policy = HashMap::new();
    let mut expe = NRPA::new();
    expe.timeout = timeout;
    expe.registerName = registerName;
    let seed = [0u8; 32]; // Valeur de seed
    let mut rng = ChaChaRng::from_seed(seed);
    let st = expe.nrpa(level, policy, ini_state, true, &mut rng);

    //let st = nrpa(level, policy, ini_state, true);
    return st;
}
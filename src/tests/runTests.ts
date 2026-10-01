import { DeterministicSimulationEngine } from '../simulation/simulationEngine';
import { SimulationScenarioId } from '../types/simulation';

function assert(condition: boolean, message: string) {
  if (!condition) {
    console.error(`❌ TEST FAILED: ${message}`);
    process.exit(1);
  } else {
    console.log(`  ✓ ${message}`);
  }
}

console.log('🚀 Running DOST Guardian 2.0 Simulation Engine Verification Suite...\n');

const engine = new DeterministicSimulationEngine();

// 1. NORMAL_OPERATION
console.log('Testing Scenario 1: NORMAL_OPERATION');
engine.loadScenario('NORMAL_OPERATION');
let state = engine.getState();
assert(state.activeScenarioId === 'NORMAL_OPERATION', 'Scenario initialized to NORMAL_OPERATION');
assert(state.workers.length > 0 && state.trains.length > 0, 'Workers and trains initialized');

// 2. TRAIN_APPROACHING
console.log('\nTesting Scenario 2: TRAIN_APPROACHING');
engine.loadScenario('TRAIN_APPROACHING');
state = engine.getState();
assert(state.trains[0].positionX === 250, 'Train positioned at X=250 approaching work zone');

// 3. MULTIPLE_WORKERS
console.log('\nTesting Scenario 3: MULTIPLE_WORKERS');
engine.loadScenario('MULTIPLE_WORKERS');
state = engine.getState();
assert(state.workers.length >= 3, 'Multiple gang maintainers present in roster');

// 4. MULTIPLE_TRAINS
console.log('\nTesting Scenario 4: MULTIPLE_TRAINS');
engine.loadScenario('MULTIPLE_TRAINS');
state = engine.getState();
assert(state.trains.length >= 2, 'Bi-directional trains active on UP & DOWN lines');

// 5. GPS_FAILURE
console.log('\nTesting Scenario 5: GPS_FAILURE');
engine.loadScenario('GPS_FAILURE');
state = engine.getState();
assert(state.workers[0].gpsAccuracyMeters === 42.0, 'GPS accuracy degraded to 42.0m');
assert(state.workers[0].envelope.isExpandedDueToGps === true, 'Dynamic safety envelope expanded');

// 6. NETWORK_FAILURE
console.log('\nTesting Scenario 6: NETWORK_FAILURE');
engine.loadScenario('NETWORK_FAILURE');
state = engine.getState();
assert(state.workers[0].networkState === 'OFFLINE', 'Worker network state set to OFFLINE');
assert(state.workers[0].status === 'DEGRADED_NETWORK', 'Worker status set to DEGRADED_NETWORK');

// 7. WORKER_UNACKNOWLEDGED
console.log('\nTesting Scenario 7: WORKER_UNACKNOWLEDGED');
engine.loadScenario('WORKER_UNACKNOWLEDGED');
state = engine.getState();
assert(state.alerts.length > 0, 'Unacknowledged alert created');
assert(state.alerts[0].escalationTier === 'TIER_1_SUPERVISOR', 'Escalated to Tier-1 Supervisor');

// 8. EMERGENCY_EVENT
console.log('\nTesting Scenario 8: EMERGENCY_EVENT');
engine.loadScenario('EMERGENCY_EVENT');
state = engine.getState();
assert(state.workers[0].status === 'EMERGENCY', 'Worker status set to EMERGENCY on manual SOS');

// 9. NEAR_MISS
console.log('\nTesting Scenario 9: NEAR_MISS');
engine.loadScenario('NEAR_MISS');
state = engine.getState();
assert(state.nearMisses.length > 0, 'Near-miss incident recorded');
assert(state.nearMisses[0].minSpatialClearanceMeters === 1.8, 'Spatial clearance breach recorded (1.8m)');

// 10. RECOVERY
console.log('\nTesting Scenario 10: RECOVERY');
engine.loadScenario('RECOVERY');
state = engine.getState();
assert(state.activeScenarioId === 'RECOVERY', 'Scenario set to RECOVERY baseline');

console.log('\n======================================================');
console.log('🎉 Core simulation engine verification tests passed.');
console.log('======================================================\n');

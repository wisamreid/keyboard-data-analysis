trig = [
201	0	0	0	0	0
202	0	0	0	0	1
203	0	0	0	1	0
204	0	0	0	1	1
205	0	0	1	0	0
206	0	0	1	0	1
207	0	0	1	1	0
208	0	0	1	1	1
209	0	1	0	0	0
210	0	1	0	0	1
211	0	1	0	1	0
212	0	1	0	1	1
213	0	1	1	0	0
214	0	1	1	0	1
215	0	1	1	1	0
216	0	1	1	1	1
217	1	0	0	0	0
218	1	0	0	0	1
219	1	0	0	1	0
220	1	0	0	1	1
221	1	0	1	0	0
222	1	0	1	0	1
223	1	0	1	1	0
224	1	0	1	1	1
225	1	1	0	0	0
226	1	1	0	0	1
227	1	1	0	1	0
228	1	1	0	1	1
229	1	1	1	0	0
230	1	1	1	0	1
231	1	1	1	1	0
232	1	1	1	1	1];

trial_trig = trig(:,1);
partner_code = trig(:,2);
task_code = trig(:,3);
order_code = trig(:,4);
devodd_code = trig(:,5);
deveven_code = trig(:,6);

save('ceo_trig_code_numbers.mat','trig','trial_trig','partner_code','task_code','order_code','devodd_code','deveven_code');


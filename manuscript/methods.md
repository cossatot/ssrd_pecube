# Methods

## Thermochronological modeling

We reconstruct the extension history of the SSR through a Bayesian inversion
incorporating the thermochronological modeling program Pecube [Braun et al.,
2012] as well as structural estimates for total strain and fault slip [e.g.,
McGrew et al., 1993] using methods derived from Styron et al., [2013]. The
inversion essentially takes random tectonothermal histories for the SSR,
filters them so they fall within structural constraints, uses Pecube to predict
thermochronometric ages for each history, and selects posterior histories based
on the goodness of fit between the predicted and observed thermochronometer
ages. This process yields joint posterior probability distributions for the
thermal and tectonic variables in the inversion.

The Bayesian approach to inversion for continuous model variables is well
described mathematically in many sources [e.g., refs] but here we will focus on
a procedural description to optimize clarity for readers less well acquainted
with the formal statistics, and use mathematical descriptions as an aide rather
than as the most compact description of the process. Bayesian inversion or
inference involves taking initial estimates of probability distributions for
each variable of interest, and then refining those estimates based on how well
predictions make by the variables compare to observations. The initial
estimates are called 'prior probabilities' or simply 'priors', and the refined
probabilites are known as 'posterior probabilities'.  Whether a distribution is
a prior or posterior distribution is solely based on whether it will be refined
in the inversion step at hand, and in many instances the posteriors for one
inversion step form the priors for another. 

The priors map to the posteriors through another distribution called the
likelihood, which encapsulates the goodness of fit between the model
predictions and the observations. This is summarized by Bayes' rule:

$ p(T|D) \propto p(T) p(D|T)$ 

where $p(T)$ is the prior probability distributions for all variables in $T$
(in our case, variables that represent the thermal and strain history);
$p(T|D)$ is the posterior probability distributions, i.e. the probability
distributions of the variables $T$ given the data $D$; and $p(D|T)$ is the
likelihood, i.e. the probability of observing the data $D$ given the parameters
$T$ are true.

### Pecube model setup

Pecube is set up somehow. We will call the Pecube model the FEM. It is based
on McGrew.

Pecube uses several variables to calculate the 'steady-state' geotherm in the
FEM, which is then perturbed by tectonic deformation: temperatures at the model
surface and base (the Moho in our FEM), thermal diffusivity, atmospheric lapse
rate, and radiogenic heat production. We fix the FEM surface temperature,
thermal diffusivity, and atmospheric lapse rate as these values are reasonably
well constrained relative to the Moho temperature and radiogenic heat
production, which we solve for in the inversion. Table X lists the values for
all parameters.

### Construction of priors

The initial step in the inversion is the construction of the priors. We wish to
solve for the coupled strain history and thermal state of the crust, so we
choose to model variables representing both of these. We separate the strain
history of the SSR into independent histories for the SSRD and WPF. These 
histories are then discretized into several time intervals with different slip
rates. The time boundaries of each slip interval and the slip rates for each
interval are all randomly sampled from uniform probability distributions. The
SSRD has four intervals between 80 and 5 Ma (note that the beginning and end
points for the entire slip history may be anywhere in this interval), and the
WPF has 3 intervals between 40 and 0 Ma. Slip rates at any time on the SSRD are
between 0 and 10 mm a$^{-1}$, and between 0 to 4 mm a$^{-1}$ on the WPF. Moho
temperatures are taken from between 600-1100 °C, and radiogenic heat production
from 5-50 °C Ma$^{-1}$. [Refs?].

This yields a prior distribution $p(T)$, where $T$ is a vector*(?)* of
probability distributions for each variable in $T$. Each $p(t)$ is
independent of the others.

### Filtering of priors to fit structural constraints

When constructing $p(T)$, we have chosen probabilities $p(t)$ for each $t$ that
are individually reasonable (or at least possible), and considered independent.
However, many combinations of the variables yield extension histories that
violate constraints from geologic cross sections. Therefore, we wish to only
consider the subset of $p(T)$ that is consistent with geological constraints,
which we call $p(T|G)$, or *the probability of T given geological constraints
G*. From a practical perspective, if we can reduce $p(T)$ to a much smaller 
(or much more sparse) $p(T|G)$ before the computationally-intensive Pecube
modeling, we can reduce total computation times by one or two orders of
magnitude with no loss of statistical robustness, as $p(t|G)$ may be very
similar to $p(t)$ for any $t$. 

A very effective way to reduce $p(T)$ to $p(T|G)$ is to filter samples from
$p(T)$ that predict net extension outside of acceptable bounds determined by
geologic cross sections [e.g, Styron et al., 2013]. We arithmetically calculate
the net extension for each sample of $p(T)$ given fault dips from the FEM and
strain history variables from the $p(T)$ sample, and accept into $p(T|G)$ only
those with net extension values between 8 and 35 km, based on [...]. We
iteratively sample and filter $p(T)$ until $p(T|G)$ has 9999 samples, which
we will run in Pecube.

### Calculating likelihood with Pecube

We use Pecube to predict thermochronometer ages at our sample locations,
in order to calculate $p(D|T)$. Pecube models were run on the Eureka cluster at
the National Supercomputing Center for Energy and the Environment at the
University of Nevada Las Vegas. Each model took between 0.5 to 2.5 hours to
compute. Parallelization of about 100x allowed us to run the ~15,000 CPU hours
of computation in a little over a week.

We evaluate each model from $p(T|G)$ by calculating the relative model
likelihood $p(D|T)$ using the equation

$p(D|T) = \frac{ \exp (- \chi^2) }{ \exp( - \chi^2_{\min})} $

where $\chi^2$ is the goodness-of-fit statistic for normally-distributed data

$\chi^2 = \frac{ 1 }{N} \Sigma^N_{i=1} \frac{ (\mu_i - \hat{\mu}_i)^2 }{\sigma_i^2} $

$\mu$ is the measured age, $\hat{\mu}$ is the modeled age, and $\sigma$ is the
measured standard deviation. Because the constant of proportionality in
equation (1) is unknown, we normalize $p(D|T)$ relative to the best-fitting
model [Tarantola, 2005].

Once the relative likelihoods have been calculated for each model, we calculate
the posterior $p(T|D)$, or 'sampling the posterior' in Bayesian terminology, by
selecting models from $p(T|G)$ proportional to their likelihood [e.g. Mosegaard
and Tarantola, 1995]. In practice this is done by selecting models whose
likelihood is larger than a number randomly sampled from the uniform
distribution [0,1) (note that this random number is generated independently for
each comparison).

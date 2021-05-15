# python implementation of Bicanski-Burgess model
#
'''
List of abbreviations:
    PCs:     place cells
    BVCs:    boundary vector cells
    OVCs:    object vector cells
    H/HPC:   hippocampus
    ID/PR:   identity neurons in perirhinal cortex, used for texture of walls.
    oID/oPR: object identiy neurons
    PW:      parietal window, contains egocentric analogs of BVCs, is "canvas" for imagery
    oPW:     parietal window, contains egocentric analogs of OVCs, is "canvas" for imagery
    MTL:     Medial Temporal Lobe (means PCs in HPC, BVCs and perirhinal ID neurons)
    RSC:     retrospenial cortex, contains tranformation circuit between PW and BVCs
    HD(Cs):  head direction (cells)
    TR:      transformation, usually refers to the RSC layers (see RSC)
    IP:      inhibitory feedback neuron
    GC:      grid cells for imagined movement


List of subroutines:

    BB_prep_connectGCs2PCs.m - prep: make connections between PCs and GCs
    BB_prep_makeGCs.m - prep: makes grid cell rate maps to generate a look-up table for grid cell firing rates
    BB_prep_makeWTS_new.m - prep: takes care of the geometry of the environment, and generates desired weights. 
    BB_prep_subr_intersection.m - prep: Figures out how far along each line two lines intersect.
    
    BB_subr_PLT_TR.m - plot
    BB_subr_PLT_fancy.m - plot
    
    BB_subr_BUvsTD.m - bottom up vs top down
    BB_subr_PR_BoundaryCueing.m - a simple routine to cue with the wall identity, which we assume the agent
        can recognize. We determine the minimum distance to each wall (N,S,E,W)
        and how many boundary points of each wall are visible. Both factors
        contribute to the PRcue during perception, which drives the PR neurons.
        This helps the model remove ambiguity in the simple 4 wall environment.
    BB_subr_PR_BoundaryCueing_with_Barrier.m - hear for more boundaries, but should be unified with the scripts 'BB_subr_PR_BoundaryCueing.m'
    BB_subr_PR_BoundaryCueing_with_Barrier_sim50.m
    BB_subr_PdrivePW_withObj.m - update boundary cells with translation
    BB_subr_PreplayOverhead.m - extra overhead for preplay/planning simulation
        changes for sealed-off part of arena introduce all this messy
        overhead, because the reservoir place cells, random connections
        from grid cell, variables for tracking activity and for plotting 
        etc. need to be defined
    BB_subr_QuantCorr.m - two situations should trigger registering firing rates for comparision:
        1. at encoding, the array ObjEncoded is incremented elsewhere in that case, 
        and only if firing rates are reasonably high, that's fine for the purpose of this subroutine
        2. at recall we should register firing rate, but we must make sure there
        was enough time for buildup of activity
    BB_subr_TrajectoryParas.m - trajectory parameters
    BB_subr_XYestimFromPCs.m - estimate position from PC activity bump to able to plot imagined position
    BB_subr_agent_model.m - returns real and imagnined location estimates based of translation and rotation
    BB_subr_allocATTinPW.m - When we imagine a object in its context, associated PCs will drive OVCs
        for all objects encoded from that location. Meaning, even if we cue with
        only one object, the other associated OVCs (for other objects relative to 
        the current location) will receive some input from PCs, leading to a 
        residual peak in OVCs not coding the position of the currently imagined
        object. This activity spreads to the PWo and can be located to allocate
        attention there. This referes to simflag 31. The function returns a
        cueing current which "allocates attention" to the residual peak.
    BB_subr_attention_enc.m - return Object cueing current for oPW and oPR rate
        latter driven by putative recognition process along ventral vis stream
        and modulated by heuristic attention
    BB_subr_cue_HDact.m - bump_locs is the initial HD, i.e. the location of the activity bump
    BB_subr_cue_PWact_multiseg.m - actually calculates something proportional
        to BVC FIRING RATE when an bndry is present. I use it to generate
        cuing current as well.
    BB_subr_radscaling.m - calculate polar distance
    BB_subr_trajectory.m - updates the linear translational movement. Rotation
        is resolved in the agent model script.
        The function needs to take care not to run into boundaries
        We use a list of targets to be visited in the arena. By arranging
        the order of the targets appropriately we avoid running into boundaries
        and avoid calculations of geometry.
    BB_subr_updateWTS.m - this function implemets simple Hebbian associations between MTL model
        components at the chosen time of encoding and saves them to the respective weight matrices

'''
import numpy as np


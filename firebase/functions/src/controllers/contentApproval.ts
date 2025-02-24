import { Request, Response } from 'express';
import { firestoreService } from '../services/firestore_service';
import { crewAIService } from '../services/crewAIService';
import { Link, Gist } from '../types';


export const contentApprovalController = {
  async fetchUserGist(req: Request, res: Response) {
    try {
      const { userId, gistId } = req.params;

      // Use firestoreService instead of direct db access
      try {
        if (gistId) {
          const { gists } = await firestoreService.getUserGists(userId);
          const gist = gists.find((g: Gist) => g.gistId === gistId);
          
          if (!gist) {
            return res.status(404).json({
              success: false,
              error: 'Gist not found'
            });
          }

          return res.status(200).json({
            success: true,
            data: gist
          });
        }

        const result = await firestoreService.getUserGists(userId);
        return res.status(200).json({
          success: true,
          data: result.gists
        });
      } catch (error: unknown) {
        if (error instanceof Error) {
          if (error.message === 'User not found') {
            return res.status(404).json({
              success: false,
              error: 'User not found'
            });
          }
        }
        throw error;
      }
    } catch (error) {
      console.error('Error fetching gist:', error);
      return res.status(500).json({
        success: false,
        error: 'Failed to fetch gist'
      });
    }
  },

  async updateGistProductionStatus(req: Request, res: Response) {
    try {
      const { userId, gistId } = req.params;
      
      // Update status using firestoreService
      const updatedGist = await firestoreService.updateGistStatus(userId, gistId, {
        in_productionQueue: true,
        production_status: 'In Production - Content Approval Pending'
      });

      // Trigger CrewAI workflow
      await crewAIService.initiateContentApproval({
        userId,
        gistId,
        gistData: updatedGist
      });

      return res.status(200).json({
        success: true,
        message: 'Gist production status updated successfully',
        data: updatedGist
      });

    } catch (error: unknown) {
      console.error('Error updating gist production status:', error);
      const message = error instanceof Error ? error.message : 'Failed to update gist production status';
      return res.status(500).json({
        success: false,
        error: message
      });
    }
  },

  async fetchUserLink(req: Request, res: Response) {
    try {
      const { userId, linkId } = req.params;

      try {
        const { links } = await firestoreService.getUserLinks(userId);
        const link = links.find((l: Link) => l.link_id === linkId);
        
        if (!link) {
          return res.status(404).json({
            success: false,
            error: 'Link not found'
          });
        }

        // Check if link is already processed
        if (link.gist_created) {
          return res.status(400).json({
            success: false,
            error: 'Link already processed into a gist'
          });
        }

        return res.status(200).json({
          success: true,
          data: link
        });

      } catch (error: any) {
        if (error.message === 'User not found') {
          return res.status(404).json({
            success: false,
            error: 'User not found'
          });
        }
        throw error;
      }
    } catch (error) {
      console.error('Error fetching link:', error);
      return res.status(500).json({
        success: false,
        error: 'Failed to fetch link'
      });
    }
  },

  // We'll add more methods here as we continue
  // - createGist
  // - updateGistStatus
  // - initiateContentApproval
};

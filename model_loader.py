"""
Optimized Model Loader for AWS Deployment
This module handles efficient loading and caching of ML models
"""

import os
import logging
from sentence_transformers import SentenceTransformer
from spellchecker import SpellChecker
import pickle
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelLoader:
    """Singleton class for loading and caching ML models"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ModelLoader, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.sentence_model = None
        self.spell_checker = None
        self.label_encoder = None
        self.resume_classifier = None
        self._initialized = True
        
        # Common tech terms for spell checker
        self.COMMON_TECH_TERMS = {
            'js', 'dev', 'github', 'linkedin', 'firebase', 'wireframe', 
            'wireframes', 'signups', 'efficiency', 'api', 'ui', 'ux',
            'sql', 'nosql', 'aws', 'gcp', 'azure', 'docker', 'kubernetes'
        }
    
    def load_sentence_transformer(self):
        """Load sentence transformer model with caching"""
        if self.sentence_model is None:
            try:
                logger.info("Loading SentenceTransformer model...")
                self.sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("SentenceTransformer model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load SentenceTransformer: {e}")
                raise
        return self.sentence_model
    
    def load_spell_checker(self):
        """Load spell checker with custom tech terms"""
        if self.spell_checker is None:
            try:
                logger.info("Loading spell checker...")
                self.spell_checker = SpellChecker()
                self.spell_checker.word_frequency.load_words(self.COMMON_TECH_TERMS)
                logger.info("Spell checker loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load spell checker: {e}")
                raise
        return self.spell_checker
    
    def load_label_encoder(self):
        """Load label encoder for resume classification"""
        if self.label_encoder is None:
            try:
                encoder_path = os.path.join('backend', 'models', 'label_encoder.pkl')
                if os.path.exists(encoder_path):
                    logger.info("Loading label encoder...")
                    with open(encoder_path, 'rb') as f:
                        self.label_encoder = pickle.load(f)
                    logger.info("Label encoder loaded successfully")
                else:
                    logger.warning(f"Label encoder not found at {encoder_path}")
            except Exception as e:
                logger.error(f"Failed to load label encoder: {e}")
        return self.label_encoder
    
    def load_resume_classifier(self):
        """Load resume classifier model"""
        if self.resume_classifier is None:
            try:
                model_path = os.path.join('backend', 'models', 'resume_classifier_roberta_large_aug')
                if os.path.exists(model_path):
                    logger.info("Loading resume classifier...")
                    # Import here to avoid loading if not needed
                    from transformers import AutoTokenizer, AutoModelForSequenceClassification
                    
                    tokenizer = AutoTokenizer.from_pretrained(model_path)
                    model = AutoModelForSequenceClassification.from_pretrained(model_path)
                    
                    self.resume_classifier = {
                        'tokenizer': tokenizer,
                        'model': model
                    }
                    logger.info("Resume classifier loaded successfully")
                else:
                    logger.warning(f"Resume classifier not found at {model_path}")
            except Exception as e:
                logger.error(f"Failed to load resume classifier: {e}")
        return self.resume_classifier
    
    def preload_all_models(self):
        """Preload all models during application startup"""
        logger.info("Preloading all models...")
        try:
            self.load_sentence_transformer()
            self.load_spell_checker()
            self.load_label_encoder()
            # Note: Resume classifier is heavy, load on-demand
            logger.info("All critical models preloaded successfully")
        except Exception as e:
            logger.error(f"Failed to preload models: {e}")
            raise

# Global model loader instance
model_loader = ModelLoader()

# Convenience functions for backward compatibility
def get_sentence_model():
    """Get the sentence transformer model"""
    return model_loader.load_sentence_transformer()

def get_spell_checker():
    """Get the spell checker"""
    return model_loader.load_spell_checker()

def get_label_encoder():
    """Get the label encoder"""
    return model_loader.load_label_encoder()

def get_resume_classifier():
    """Get the resume classifier"""
    return model_loader.load_resume_classifier()

def preload_models():
    """Preload all models"""
    model_loader.preload_all_models()

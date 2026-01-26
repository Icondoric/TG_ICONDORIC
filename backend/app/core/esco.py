import csv
import os
import re
from typing import Dict, List, Set, Tuple, Any
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc

# Path to the data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

class ESCOLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ESCOLoader, cls).__new__(cls)
            # Mappings for search
            cls._instance.skills_map = {}      # keyword -> {label, uri, type}
            cls._instance.occupations_map = {} # keyword -> {label, uri}
            
            # Sets for categorization (Storage of URIs)
            cls._instance.digital_skills = set()
            cls._instance.language_skills = set()
            cls._instance.transversal_skills = set()
            cls._instance.green_skills = set()
            
            cls._instance.green_skills = set()
            
            # BLACKLIST: Common words that exist in ESCO/Tools but create noise
            cls._instance.blacklist = {
                "panorama", "plan", "go", "r", "c", "bases", "marco", "activos", "valor", "valores",
                "equipo", "equipos", "part", "total", "fuerza", "saber", "ser", "estar",
                "gestion", "gestión", "empresa", "empresas", "grupo", "misión", "vision",
                "industrial", "textil", # If generic "textil" is causing issues
                "bolsa", "mercado", "formación", "curso", "cursos",
                "lengua", "idioma", "nivel", "alto", "bajo", "medio"
            }
            
            cls._instance.matcher = None
            cls._instance.loaded = False
        return cls._instance

    def load_data(self):
        """
        Loads ESCO datasets from CSV files into memory.
        """
        if self.loaded:
            return

        print("Loading ESCO datasets...")
        
        # 1. Load Skill Collections (to tag skills later)
        self._load_collection("digitalSkillsCollection_es.csv", self.digital_skills)
        self._load_collection("digCompSkillsCollection_es.csv", self.digital_skills) # Merge digComp into digital
        self._load_collection("languageSkillsCollection_es.csv", self.language_skills)
        self._load_collection("transversalSkillsCollection_es.csv", self.transversal_skills)
        self._load_collection("greenSkillsCollection_es.csv", self.green_skills)
        
        # 2. Load Skills
        self._load_skills()
        
        # 3. Load Occupations
        self._load_occupations()
        
        # 4. Load Tech Tools (StackShare)
        self._load_tools()

        self.loaded = True
        print("ESCO datasets loaded.")

    def _load_collection(self, filename: str, target_set: Set[str]):
        """Load URIs from a collection CSV."""
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    uri = row.get('conceptUri')
                    if uri:
                        target_set.add(uri)
        except Exception as e:
            print(f"Error loading collection {filename}: {e}")

    def _load_skills(self):
        """Load skills_es.csv"""
        path = os.path.join(DATA_DIR, "skills_es.csv")
        if not os.path.exists(path):
            print(f"ERROR: Skills file not found at {path}")
            return
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    preferred_label = row.get('preferredLabel', '').strip()
                    uri = row.get('conceptUri', '')
                    alt_labels_raw = row.get('altLabels', '')
                    
                    if not preferred_label: continue
                    
                    # Determine categories
                    categories = []
                    if uri in self.digital_skills: categories.append("digital")
                    if uri in self.language_skills: categories.append("language")
                    if uri in self.transversal_skills: categories.append("transversal")
                    if uri in self.green_skills: categories.append("green")
                    
                    # Normalize and add preferred label
                    self._add_keyword(self.skills_map, preferred_label, preferred_label, uri, categories)
                    
                    # Normalize and add alt labels
                    if alt_labels_raw:
                        alt_labels = [l.strip() for l in alt_labels_raw.split('\n') if l.strip()]
                        for alt in alt_labels:
                            self._add_keyword(self.skills_map, alt, preferred_label, uri, categories)
                    count += 1
                print(f"Loaded {count} skills.")
        except Exception as e:
            print(f"Error loading skills: {e}")

    def _load_occupations(self):
        """Load occupations_es.csv"""
        path = os.path.join(DATA_DIR, "occupations_es.csv")
        if not os.path.exists(path): return
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    preferred_label = row.get('preferredLabel', '').strip()
                    uri = row.get('conceptUri', '')
                    alt_labels_raw = row.get('altLabels', '')
                    
                    if not preferred_label: continue
                    
                    self._add_keyword(self.occupations_map, preferred_label, preferred_label, uri, ["occupation"])
                    
                    if alt_labels_raw:
                        alt_labels = [l.strip() for l in alt_labels_raw.split('\n') if l.strip()]
                        for alt in alt_labels:
                            self._add_keyword(self.occupations_map, alt, preferred_label, uri, ["occupation"])
                    count += 1
                print(f"Loaded {count} occupations.")
                
                # 4. Load Manual Aliases (Bootstrap common missing terms)
                self._load_manual_aliases()
                
        except Exception as e:
            print(f"Error loading occupations: {e}")

    def _load_tools(self):
        """Load tools.csv from StackShare dataset."""
        path = os.path.join(DATA_DIR, "tools.csv")
        if not os.path.exists(path): return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    name = row.get('name', '').strip()
                    url = row.get('url', '')
                    category = row.get('category', '').lower()
                    layer = row.get('layer', '').lower()
                    
                    if not name: continue
                    
                    # Construct categories
                    cats = ["tech_tool"]
                    if category: cats.append(category)
                    if layer: cats.append(layer)
                    
                    # Add to map
                    self._add_keyword(self.skills_map, name, name, url, cats)
                    count += 1
                print(f"Loaded {count} tech tools from StackShare.")
        except Exception as e:
            print(f"Error loading tools: {e}")

    def _load_manual_aliases(self):
        """Inject common terms that might be hard to find in ESCO."""
        aliases = {
            "sql": {"label": "SQL", "uri": "custom:sql", "categories": ["digital"]},
            "python": {"label": "Python", "uri": "http://data.europa.eu/esco/skill/python", "categories": ["digital"]}, # Ensure simple Python is there
            "liderazgo": {"label": "Liderazgo", "uri": "custom:leadership", "categories": ["transversal"]},
            "trabajo en equipo": {"label": "Trabajo en equipo", "uri": "custom:teamwork", "categories": ["transversal"]},
            "trabajar en equipo": {"label": "Trabajo en equipo", "uri": "custom:teamwork", "categories": ["transversal"]}, # Override "Textile" variant
            "comunicación": {"label": "Comunicación", "uri": "custom:communication", "categories": ["transversal"]},
            "inglés": {"label": "Inglés", "uri": "http://data.europa.eu/esco/skill/english", "categories": ["language"]}
        }
        
        for key, data in aliases.items():
            # Only add if not already present or to ensure simplified access
            # We use _add_keyword to handle normalization
            self._add_keyword(self.skills_map, key, data["label"], data["uri"], data["categories"])

    def _add_keyword(self, target_map: Dict, keyword: str, canonical: str, uri: str, categories: List[str]):
        """Helper to add mappings with heuristics."""
        cleaned_key = self._normalize_text(keyword)
        if not cleaned_key: return
        
        # Blacklist check (exact match)
        if cleaned_key in self.blacklist:
            return
            
        # Ignore very short keys (1-2 chars) unless whitelisted (like C, R - though usually handled by known_tech)
        # But for now, we just skip 1 char to be safe
        if len(cleaned_key) < 2: 
             return
            
        target_map[cleaned_key] = {
            "label": canonical,
            "uri": uri,
            "categories": categories
        }
        
        # Parenthesis Heuristic
        if '(' in cleaned_key:
            simple_key = re.sub(r'\s*\(.*?\)', '', cleaned_key).strip()
            if simple_key and simple_key != cleaned_key and simple_key not in target_map:
                target_map[simple_key] = {
                    "label": canonical,
                    "uri": uri,
                    "categories": categories
                }

    def _normalize_text(self, text: str) -> str:
        # Lowercase and strip whitespace
        text = text.lower().strip()
        # Remove basic punctuation to ensure clean token matching
        text = re.sub(r'[.,;()\[\]{}"\':?!-]', ' ', text)
        return re.sub(r'\s+', ' ', text).strip()

    def search_items(self, text: str) -> Dict[str, List[Dict]]:
        """
        Searches for both skills and occupations in the text.
        Returns unified results.
        """
        normalized_text = self._normalize_text(text)
        found_skills = {}
        found_occupations = {}
        
        words = normalized_text.split()
        n = len(words)
        MAX_NGRAM = 6 # Increase slightly for longer occupation titles
        
        for i in range(n):
            for length in range(1, MAX_NGRAM + 1):
                if i + length > n: break
                
                phrase = " ".join(words[i : i + length])
                
                # Check Skills
                if phrase in self.skills_map:
                    match = self.skills_map[phrase]
                    found_skills[match['label']] = match
                    
                # Check Occupations
                if phrase in self.occupations_map:
                    match = self.occupations_map[phrase]
                    found_occupations[match['label']] = match
        
        return {
            "skills": list(found_skills.values()),
            "occupations": list(found_occupations.values())
        }

    def build_matcher(self, nlp):
        """
        Builds specific patterns for Spacy PhraseMatcher.
        This allows for much faster and token-aware matching (avoiding 'Go' in 'Google').
        """
        if self.matcher: return
            
        print("Building Spacy PhraseMatcher for Skills & Occupations...")
        self.matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        
        # We need to collect patterns
        # 1. Skills
        skill_patterns = list(self.skills_map.keys())
        # Convert strings to Doc objects (efficiently via pipe if list is huge, but here map is okay)
        # Using nlp.make_doc is faster than nlp() as it skips pipeline
        skill_docs = [nlp.make_doc(text) for text in skill_patterns]
        self.matcher.add("SKILL", skill_docs)
        
        # 2. Occupations
        occ_patterns = list(self.occupations_map.keys())
        occ_docs = [nlp.make_doc(text) for text in occ_patterns]
        self.matcher.add("OCCUPATION", occ_docs)
        
        print(f"Matcher built with {len(skill_docs)} skills and {len(occ_docs)} occupations rules.")

    def search_items_spacy(self, doc: Doc) -> Dict[str, List[Dict]]:
        """
        Uses the pre-built PhraseMatcher on a Spacy Doc object.
        """
        if not self.matcher:
            # Fallback or error - but we expect built_matcher to be called
            return self.search_items(doc.text)

        matches = self.matcher(doc)
        found_skills = {}
        found_occupations = {}

        # Pre-compute Entity Spans to avoid overlaps (e.g. don't match skill inside a Person Name)
        # We assume entities like PER, ORG, LOC might contain generic words we want to ignore if matched as skill
        entity_ranges = []
        for ent in doc.ents:
            if ent.label_ in ["PER", "LOC", "ORG", "DATE"]:
               entity_ranges.append((ent.start, ent.end))

        for match_id, start, end in matches:
            span = doc[start:end]
            
            # --- FILTER 1: Entity Overlap ---
            # If the match is completely inside a named entity, skip it.
            # e.g. "Jordan" (Country/Name) vs "Jordan" (Library)
            is_inside_entity = False
            for ent_start, ent_end in entity_ranges:
                if start >= ent_start and end <= ent_end:
                    is_inside_entity = True
                    break
            if is_inside_entity:
                continue

            # --- FILTER 2: POS Tagging (Part of Speech) ---
            # Single tokens: check if it's a Verb, Adposition, etc.
            # Multi tokens: generally safer, but if it starts/ends with verb it might be "To Design"
            
            # Strict mode for single words
            if len(span) == 1:
                token = span[0]
                # Reject Verbs, Auxiliaries, Pronouns, Particles, Determiners
                # KEEP: NOUN, PROPN, ADJ (sometimes)
                if token.pos_ in ["VERB", "AUX", "ADP", "PRON", "DET", "SCONJ", "CCONJ"]:
                    continue
                
                # Special check for "Plan", "Design" etc which can be Noun or Verb
                # If spacy says it's a VERB, we trust it and skip.
                
                # Length Filter for short words (2-3 chars)
                # Must be Proper Noun to be accepted (like "Go", "R")
                if len(token.text) < 4 and token.pos_ != "PROPN":
                     # Exceptions: C (lang), R (lang) are often capitalized or found via other means
                     # If it's just "ir a C", 'C' might be noun but it's risky
                     pass 

            # Match Logic (Same as before)
            match_text = span.text.lower() # matcher uses LOWER attribute
            
            # Let's clean the span text to match our normalization
            cleaned_span = self._normalize_text(span.text)
            
            if self.matcher.vocab.strings[match_id] == "SKILL":
                if cleaned_span in self.skills_map:
                    match_data = self.skills_map[cleaned_span]
                    found_skills[match_data['label']] = match_data
            
            elif self.matcher.vocab.strings[match_id] == "OCCUPATION":
                if cleaned_span in self.occupations_map:
                    match_data = self.occupations_map[cleaned_span]
                    found_occupations[match_data['label']] = match_data

        return {
            "skills": list(found_skills.values()),
            "occupations": list(found_occupations.values())
        }


# Global instance
esco_loader = ESCOLoader()

